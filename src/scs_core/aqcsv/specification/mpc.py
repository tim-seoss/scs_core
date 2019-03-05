"""
Created on 4 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

AQCSV: Measurement performance characteristics

NB: initialisation is performed at the foot of this class

example:
{"code": "3", "abbreviation": "XD", "definition": "Minimum Detectable Value",
"description": "The measure of inherent detection capability of a measurement process."}
"""

import os

from collections import OrderedDict

from scs_core.csv.csv_archive import CSVArchive
from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class MPC(JSONable, CSVArchive):
    """
    classdocs
    """

    _retrieved = {}

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def archive_location(cls):
        return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'archive', 'mcps.csv')


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        code = jdict.get('code')
        abbreviation = jdict.get('abbreviation')
        definition = jdict.get('definition')
        description = str(jdict.get('description'))

        return MPC(code, abbreviation, definition, description)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, code, abbreviation, definition, description):
        """
        Constructor
        """
        self.__code = code                                      # string
        self.__abbreviation = abbreviation                      # string
        self.__definition = definition                          # string
        self.__description = description                        # string


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['code'] = self.code
        jdict['abbreviation'] = self.abbreviation
        jdict['definition'] = self.definition
        jdict['description'] = self.description

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pk(self):
        return self.code


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def code(self):
        return self.__code


    @property
    def abbreviation(self):
        return self.__abbreviation


    @property
    def definition(self):
        return self.__definition


    @property
    def description(self):
        return self.__description


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "MPC:{code:%s, abbreviation:%s, definition:%s, description:%s}" % \
               (self.code, self.abbreviation, self.definition, self.description)


# --------------------------------------------------------------------------------------------------------------------
# initialisation...

MPC.retrieve()
