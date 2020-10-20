"""
Created on 20 Oct 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os
import time

from abc import ABC, abstractmethod

from scs_core.data.crypt import Crypt
from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class PersistenceManager(ABC):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def exists(self, dirname, filename):
        pass


    @abstractmethod
    def load(self, dirname, filename, encryption_key=None):
        pass


    @abstractmethod
    def save(self, jstr, dirname, filename, encryption_key=None):
        pass


    @abstractmethod
    def remove(self, dirname, filename):
        pass


# --------------------------------------------------------------------------------------------------------------------

class FilesystemPersistenceManager(PersistenceManager):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def exists(cls, dirname, filename):
        abs_filename = cls.__abs_filename(dirname, filename)

        return os.path.isfile(abs_filename)


    @classmethod
    def load(cls, dirname, filename, encryption_key=None):
        abs_filename = cls.__abs_filename(dirname, filename)

        try:
            with open(abs_filename, "r") as f:
                text = f.read()

            jstr = text if encryption_key is None else Crypt.decrypt(encryption_key, text)

        except FileNotFoundError:
            return None

        return jstr


    def save(self, jstr, dirname, filename, encryption_key=None):
        abs_dirname = self.__abs_dirname(dirname)
        abs_filename = self.__abs_filename(dirname, filename)

        # file...
        if filename:
            Filesystem.mkdir(abs_dirname)

        tmp_filename = '.'.join((abs_filename, str(int(time.time()))))

        text = jstr + '\n' if encryption_key is None else Crypt.encrypt(encryption_key, jstr)

        with open(tmp_filename, "w") as f:
            f.write(text)

        # atomic operation...
        os.rename(tmp_filename, abs_filename)


    @classmethod
    def remove(cls, dirname, filename):
        abs_filename = cls.__abs_filename(dirname, filename)

        try:
            os.remove(abs_filename)
        except FileNotFoundError:
            pass


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __abs_filename(cls, dirname, filename):
        return os.path.join(cls.scs_path(), dirname, filename)


    @classmethod
    def __abs_dirname(cls, dirname):
        return os.path.join(cls.scs_path(), dirname)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def scs_path(cls):
        pass
