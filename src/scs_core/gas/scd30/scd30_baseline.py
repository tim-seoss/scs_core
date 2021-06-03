"""
Created on 2 Jun 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

example JSON:
{"sn": {"calibrated-on": "2019-02-02T11:34:16Z", "offset": 50, "env": {"hmd": 66.0, "tmp": 11.0, "pA": 99.0}}}
"""

from collections import OrderedDict

from scs_core.data.json import PersistentJSONable
from scs_core.gas.sensor_baseline import SensorBaseline


# --------------------------------------------------------------------------------------------------------------------

class SCD30Baseline(PersistentJSONable):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    __FILENAME =    "scd30_baseline.json"

    @classmethod
    def persistence_location(cls):
        return cls.conf_dir(), cls.__FILENAME


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict, default=True):
        if not jdict:
            return None if default is None else cls(SensorBaseline(None, 0, None))

        sensor_baseline = SensorBaseline.construct_from_jdict(jdict['sn'])

        return cls(sensor_baseline)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, sensor_baseline):
        """
        Constructor
        """
        self.__sensor_baseline = sensor_baseline            # SensorBaseline


    def __eq__(self, other):
        try:
            return self.sensor_baseline == other.sensor_baseline

        except (TypeError, AttributeError):
            return False


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['sn'] = self.__sensor_baseline

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def sensor_baseline(self):
        return self.__sensor_baseline


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "SCD30Baseline:{sensor_baseline:%s}" % self.__sensor_baseline