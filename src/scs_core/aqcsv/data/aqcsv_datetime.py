"""
Created on 5 Mar 2019

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import pytz
import re

from datetime import datetime as dt, timedelta as td, timezone as tz

from scs_core.data.json import JSONable


# --------------------------------------------------------------------------------------------------------------------

class AQCSVDatetime(JSONable):
    """
    classdocs
    """

    @classmethod
    def construct_from_jstr(cls, jstr):
        match = re.match('(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})(([+\-])(\d{2})(\d{2}))?', jstr)

        if match is None:
            return None

        fields = match.groups()

        # datetime...
        year = int(fields[0])
        month = int(fields[1])
        day = int(fields[2])

        hour = int(fields[3])
        minute = int(fields[4])

        # no zone...
        if fields[5] is None:
            datetime = dt(year, month, day, hour, minute, 0, 0, tzinfo=pytz.timezone('Etc/UTC'))

            return AQCSVDatetime(datetime, None)

        # zone...
        zone_sign = -1 if fields[6] == '-' else 1
        zone_hours = int(fields[7])
        zone_mins = int(fields[8])

        zone_offset = zone_sign * td(hours=zone_hours, minutes=zone_mins)
        zone = tz(zone_offset)

        datetime = dt(year, month, day, hour, minute, 0, 0, tzinfo=zone)

        return AQCSVDatetime(datetime, zone)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, datetime, reporting_zone=None):
        """
        Constructor
        """
        self.__datetime = datetime
        self.__reporting_zone = reporting_zone


    def __hash__(self):
        return hash(self.localised())


    def __eq__(self, other):
        return self.datetime == other.datetime


    def __ge__(self, other):
        return self.datetime >= other.datetime


    def __gt__(self, other):
        return self.datetime > other.datetime


    def __le__(self, other):
        return self.datetime <= other.datetime


    def __lt__(self, other):
        return self.datetime < other.datetime


    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        if self.reporting_zone is None:
            datetime = self.datetime.astimezone(pytz.timezone('Etc/UTC'))
            return datetime.strftime("%Y%m%dT%H%M")

        datetime = self.localised()

        return datetime.strftime("%Y%m%dT%H%M%z")


    # ----------------------------------------------------------------------------------------------------------------

    def localised(self):
        return self.datetime.astimezone(self.__reporting_zone)


    def filename(self):
        datetime = self.datetime.astimezone(pytz.timezone('Etc/UTC'))
        return datetime.strftime("%Y%m%d%H%M")


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def datetime(self):
        return self.__datetime


    @property
    def reporting_zone(self):
        return self.__reporting_zone


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "AQCSVDatetime:{datetime:%s, reporting_zone:%s}" % (self.datetime, self.reporting_zone)
