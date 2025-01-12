"""
Created on 25 Dec 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Equivalent to cURLs:
curl "https://aws.southcoastscience.com/device-topics?topic=south-coast-science-dev/alphasense/loc/303/gases"
curl "https://aws.southcoastscience.com/device-topics?device=scs-bgx-303"
"""

from urllib.parse import parse_qs, urlparse

from scs_core.aws.client.api_client import APIClient
from scs_core.aws.data.byline import Byline, DeviceBylineGroup, TopicBylineGroup


# --------------------------------------------------------------------------------------------------------------------

class BylineManager(APIClient):
    """
    classdocs
    """

    # __URL = 'https://aws.southcoastscience.com/device-topics'
    __URL = 'https://cxzne688y0.execute-api.us-west-2.amazonaws.com/default/Bylines'

    __DEVICE =      'device'
    __TOPIC =       'topic'


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client, reporter=None):
        super().__init__(http_client)

        self.__reporter = reporter                              # BatchDownloadReporter


    # ----------------------------------------------------------------------------------------------------------------

    def find_latest_byline_for_topic(self, topic):
        params = {self.__TOPIC: topic}

        response = self._http_client.get(self.__URL, params=params)
        jdict = response.json()

        # bylines...
        if jdict is None:
            return None

        latest_byline = None

        for item in jdict:
            byline = Byline.construct_from_jdict(item)

            if latest_byline is None or latest_byline.rec < byline.rec:
                latest_byline = byline

        return latest_byline


    def find_bylines(self, excluded=None):
        params = {}
        items_jdict = []

        while True:
            response = self._http_client.get(self.__URL, params=params)
            jdict = response.json()

            block = jdict.get('Items')
            items_jdict += block

            # report...
            if self.__reporter:
                self.__reporter.print(len(block))

            # next...
            if jdict.get('next') is None:
                break

            next_url = urlparse(jdict.get('next'))
            params = parse_qs(next_url.query)

        # bylines...
        return TopicBylineGroup.construct_from_jdict(items_jdict, excluded=excluded, skeleton=True)


    def find_bylines_for_topic(self, topic, excluded=None):
        params = {self.__TOPIC: topic}

        response = self._http_client.get(self.__URL, params=params)
        self._check_response(response)

        jdict = response.json()

        # bylines...
        return TopicBylineGroup.construct_from_jdict(jdict, excluded=excluded, skeleton=True)


    def find_bylines_for_device(self, device, excluded=None):
        params = {self.__DEVICE: device}

        response = self._http_client.get(self.__URL, params=params)
        self._check_response(response)

        jdict = response.json()

        # bylines...
        return DeviceBylineGroup.construct_from_jdict(jdict, excluded=excluded, skeleton=True)


    def find_byline_for_device_topic(self, device, topic):
        params = {self.__DEVICE: device}

        response = self._http_client.get(self.__URL, params=params)
        self._check_response(response)

        jdict = response.json()

        # bylines...
        if jdict is None:
            return None

        for item in jdict:
            byline = Byline.construct_from_jdict(item)

            if byline.topic == topic:
                return byline

        return None


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "BylineManager:{reporter:%s}" % self.__reporter
