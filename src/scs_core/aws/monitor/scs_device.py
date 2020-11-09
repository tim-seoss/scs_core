"""
Created on 29 Sep 2020

@author: Jade Page (jade.page@southcoastscience.com)
"""
from collections import OrderedDict

# --------------------------------------------------------------------------------------------------------------------
from scs_core.data.json import JSONable


class SCSDevice(JSONable):
    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_jdict(cls, jdict):
        if not jdict:
            return None

        device_tag = jdict.get('dev-tag')
        email_list = jdict.get('email')
        status_active = jdict.get("status")

        return SCSDevice(device_tag, email_list, status_active)

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, device_tag, email_list, is_active, bylines=None):
        """
        Constructor
        """
        self.__latest_pub = None
        self.__dm_status = ""  # for device monitor use only
        self.__device_tag = device_tag
        self.__email_list = email_list
        self.__is_active = is_active
        self.__bylines = bylines
        self.__uptime = None
        self.__byline_status = None
        self.__email_sent = False
        self.__old_uptime = None


    # ----------------------------------------------------------------------------------------------------------------
    @property
    def device_tag(self):
        return self.__device_tag

    @property
    def email_sent(self):
        return self.__email_sent

    @property
    def email_list(self):
        return self.__email_list

    @property
    def bylines(self):
        return self.__bylines

    @property
    def uptime(self):
        return self.__uptime

    @property
    def old_uptime(self):
        return self.__old_uptime

    @property
    def is_active(self):
        return self.__is_active

    @property
    def dm_status(self):
        return self.__dm_status

    @property
    def latest_pub(self):
        return self.__latest_pub

    @property
    def byline_status(self):
        return self.__byline_status

    @latest_pub.setter
    def latest_pub(self, latest_pub):
        self.__latest_pub = latest_pub

    @dm_status.setter
    def dm_status(self, dm_status):
        self.__dm_status = dm_status

    @is_active.setter
    def is_active(self, status_active):
        self.__is_active = status_active

    @uptime.setter
    def uptime(self, uptime):
        self.__uptime = uptime

    @old_uptime.setter
    def old_uptime(self, old_uptime):
        self.__old_uptime = old_uptime

    @byline_status.setter
    def byline_status(self, byline_status):
        self.__byline_status = byline_status

    @email_sent.setter
    def email_sent(self, email_sent):
        self.__email_sent = email_sent

    # ----------------------------------------------------------------------------------------------------------------

    def as_json(self):
        jdict = OrderedDict()

        jdict['dev-tag'] = self.__device_tag
        jdict['email'] = self.__email_list
        jdict["status-active"] = self.__is_active
        jdict["latest-pub"] = self.__latest_pub
        jdict["dm-status"] = self.__dm_status
        jdict["bylines"] = self.__bylines
        jdict["uptime"] = self.__uptime
        jdict["byline_status"] = self.__byline_status

        return jdict

    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "DeviceLine:{dev-tag: %s, email: %s, status-active:%s}" % \
               (SCSDevice.device_tag, SCSDevice.email_list, SCSDevice.is_active)
