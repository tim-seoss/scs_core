"""
Created on 3 May 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
"""

import os

from collections import OrderedDict
from importlib import import_module

from scs_core.data.json import JSONable
from scs_core.data.str import Str

from scs_core.estate.git_pull import GitPull

from scs_core.sys.filesystem import Filesystem


# --------------------------------------------------------------------------------------------------------------------

class PackageVersion(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_installation(cls, package, repository):
        try:
            module = import_module(package)
        except ModuleNotFoundError:
            return cls(repository, None)

        try:
            # noinspection PyUnresolvedReferences
            version = module.__version__
        except AttributeError:
            version = None

        return cls(repository, version)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        repository = jdict.get('repo')
        version = jdict.get('version')

        return cls(repository, version)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, repository, version):
        """
        Constructor
        """
        self.__repository = repository              # string
        self.__version = version                    # string


    def __eq__(self, other):
        try:
            return self.repository == other.repository and self.version == other.version
        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def repository(self):
        return self.__repository


    @property
    def version(self):
        return self.__version


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['repo'] = self.repository
        jdict['version'] = self.version

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PackageVersion:{repository:%s, version:%s}" %  (self.repository, self.version)


# --------------------------------------------------------------------------------------------------------------------

class PackageVersions(JSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_installation(cls, root):
        versions = OrderedDict()

        for repository in GitPull.dirs(root):
            contents = Filesystem.ls(os.path.join(root, repository, 'src'))

            for content in contents:
                package = content.name
                versions[package] = (PackageVersion.construct_from_installation(package, repository))

        return cls(versions)


    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        versions = OrderedDict()

        for package, version in jdict.items():
            versions[package] = PackageVersion.construct_from_jdict(version)

        return cls(versions)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, versions):
        """
        Constructor
        """
        self.__versions = versions                  # OrderedDict of package: PackageVersion


    def __len__(self):
        return len(self.versions)


    def __eq__(self, other):
        try:
            if len(self) != len(other):
                return False

            for package in self.__versions.keys():
                if self.__versions[package] != other.__versions[package]:
                    return False

            return True

        except (KeyError, TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def versions(self):
        return self.__versions


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        return self.versions


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PackageVersions:{versions:%s}" %  Str.collection(self.versions)
