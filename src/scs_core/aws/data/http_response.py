"""
Created on 23 Apr 2021

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

https://docs.python.org/3/library/http.html
https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
"""

from abc import ABC
from http import HTTPStatus

from scs_core.data.json import JSONable, JSONify

from scs_core.sys.http_exception import HTTPException


# --------------------------------------------------------------------------------------------------------------------

class HTTPResponse(JSONable, ABC):
    """
    classdocs
    """

    __CORS_HEADERS = {                                  # Cross-Origin Resource Sharing
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Credentials': True,
    }


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def construct_from_response(cls, response):
        status = HTTPStatus(response.status_code)

        if status != HTTPStatus.OK:
            raise HTTPException(status.value, response.reason, response.json())

        jdict = response.json()

        if not jdict:
            return None

        return cls.construct_from_response_jdict(status, jdict)


    @classmethod
    def construct_from_response_jdict(cls, status, jdict):
        return cls(status)


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, status, reason=None):
        """
        Constructor
        """
        self.__status = status                          # HTTPStatus member
        self.__reason = reason                          # string


    # ----------------------------------------------------------------------------------------------------------------

    def is_ok(self):
        return self.status == HTTPStatus.OK


    # ----------------------------------------------------------------------------------------------------------------

    def as_http(self, cors=False):
        jdict = {
            'statusCode': self.status.value,
            'body': JSONify.dumps(self)
        }

        if cors:
            jdict['headers'] = self.__CORS_HEADERS

        return jdict


    def as_json(self):
        reason = self.status.description if self.reason is None else self.reason

        jdict = {
            'statusCode': self.status.value,
            'body': reason
        }

        return jdict


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def status(self):
        return self.__status


    @property
    def reason(self):
        return self.__reason


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "HTTPResponse:{status:%s, reason:%s}" % (self.status, self.reason)
