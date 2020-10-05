"""
Created on 13 Aug 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json
import os
import time

from abc import abstractmethod
from collections import OrderedDict

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class JSONify(json.JSONEncoder):
    """
    classdocs
    """

    @staticmethod
    def dumps(obj, skipkeys=False, ensure_ascii=False, check_circular=True,
              allow_nan=True, cls=None, indent=None, separators=None,
              default=None, sort_keys=False, **kw):

        handler = JSONify if cls is None else cls

        return json.dumps(obj, skipkeys=skipkeys, ensure_ascii=ensure_ascii, check_circular=check_circular,
                          allow_nan=allow_nan, cls=handler, indent=indent, separators=separators,
                          default=default, sort_keys=sort_keys, **kw)


    # ----------------------------------------------------------------------------------------------------------------

    def default(self, obj):
        if isinstance(obj, JSONable):
            return obj.as_json()

        return json.JSONEncoder.default(self, obj)


# --------------------------------------------------------------------------------------------------------------------

class JSONable(object):
    """
    classdocs
    """

    _INDENT = 4

    # ----------------------------------------------------------------------------------------------------------------

    def as_list(self, jlist):
        del jlist[:]                                    # empty the list

        for key, value in self.as_json().items():
            try:
                value = value.as_json()
            except AttributeError:
                pass

            jlist.append((key, value))                  # append the key-value pairs of the dictionary


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def as_json(self, *args, **kwargs):                 # TODO: handle named parameters of JSONify.dumps(..)
        pass


# --------------------------------------------------------------------------------------------------------------------

class JSONReport(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load(cls, filename):
        if filename is None:
            return None

        if not os.path.isfile(filename):
            return cls.construct_from_jdict(None)

        f = open(filename, 'r')
        jstr = f.readline()
        f.close()

        jdict = json.loads(jstr)

        return cls.construct_from_jdict(jdict)


    @classmethod
    def delete(cls, filename):
        if filename is None:
            return

        os.remove(filename)


    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, _):
        return JSONReport()


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, filename):
        if filename is None:
            return

        # data...
        jstr = JSONify.dumps(self, indent=self._INDENT)

        # file...
        tmp_filename = '.'.join((filename, str(int(time.time()))))

        try:
            f = open(tmp_filename, 'w')
            f.write(jstr + '\n')
            f.close()

        except FileNotFoundError:           # the containing directory does not exist (yet)
            return False

        # atomic operation...
        os.rename(tmp_filename, filename)

        return True


# --------------------------------------------------------------------------------------------------------------------

class AbstractPersistentJSONable(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _load_jstr_from_file(abs_filename):
        with open(abs_filename, "r") as f:                  # may raise FileNotFoundError
            jstr = f.read()

        return jstr.strip()


    @staticmethod
    def _save_jstr_to_file(jstr, directory, rel_filename=None):
        # file...
        if rel_filename:
            Filesystem.mkdir(directory)

        abs_filename = os.path.join(directory, rel_filename) if rel_filename else directory
        tmp_filename = '.'.join((abs_filename, str(int(time.time()))))

        with open(tmp_filename, "w") as f:
            f.write(jstr.strip())

        # atomic operation...
        os.rename(tmp_filename, abs_filename)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load_from_file(cls, filename):
        try:
            jstr = cls._load_jstr_from_file(filename)
        except FileNotFoundError:
            return cls.construct_from_jdict(None)

        return cls.construct_from_jdict(json.loads(jstr, object_hook=OrderedDict))


    @classmethod
    @abstractmethod
    def construct_from_jdict(cls, _jdict):
        return PersistentJSONable()


    # ----------------------------------------------------------------------------------------------------------------

    @abstractmethod
    def save(self, host):
        pass


# --------------------------------------------------------------------------------------------------------------------

class PersistentJSONable(AbstractPersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load(cls, host):
        try:
            filename = os.path.join(*cls.persistence_location(host))
        except NotImplementedError:
            return None

        return cls.load_from_file(filename)


    @classmethod
    def delete(cls, host):
        try:
            os.remove(os.path.join(*cls.persistence_location(host)))
            return True

        except FileNotFoundError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def persistence_location(cls, host):
        return None, None


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        self.save_to_file(*self.persistence_location(host))


    def save_to_file(self, directory, filename=None):               # TODO: make this private
        jstr = JSONify.dumps(self, indent=self._INDENT)

        self._save_jstr_to_file(jstr, directory, rel_filename=filename)


# --------------------------------------------------------------------------------------------------------------------

class MultiPersistentJSONable(AbstractPersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def load(cls, host, name):
        try:
            filename = os.path.join(*cls.persistence_location(host, name))
        except NotImplementedError:
            return None

        try:
            jstr = cls._load_jstr_from_file(filename)
        except FileNotFoundError:
            return cls.construct_from_jdict(None)

        return cls.construct_from_jdict(json.loads(jstr, object_hook=OrderedDict))


    @classmethod
    def delete(cls, host, name):
        try:
            os.remove(os.path.join(*cls.persistence_location(host, name)))
            return True

        except FileNotFoundError:
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    @abstractmethod
    def persistence_location(cls, host, name):
        return None, None


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, name):
        self.__name = name                                          # string


    # ----------------------------------------------------------------------------------------------------------------

    def save(self, host):
        jstr = JSONify.dumps(self, indent=self._INDENT)
        directory, filename = self.persistence_location(host, self.name)

        self._save_jstr_to_file(jstr, directory, rel_filename=filename)


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def name(self):
        return self.__name


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MultiPersistentJSONable:{name:%s}" % self.name
