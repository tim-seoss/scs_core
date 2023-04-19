"""
Created on 19 Apr 2023

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from http import HTTPStatus

from scs_core.sys.http_exception import HTTPException
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------

class APIClient(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, http_client):
        """
        Constructor
        """
        self.__http_client = http_client                        # requests package
        self.__logger = Logging.getLogger()


    # ----------------------------------------------------------------------------------------------------------------

    def _headers(self, token):
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json", "Token": token}
        self.__logger.debug('headers: %s' % headers)

        return headers


    def _check_response(self, response):
        self.__logger.debug('response: %s' % response.json())

        status = HTTPStatus(response.status_code)

        if status != HTTPStatus.OK:
            raise HTTPException.construct(status.value, response.reason, response.json())


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def _http_client(self):
        return self.__http_client


    @property
    def _logger(self):
        return self.__logger


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return self.__class__.__name__ + ":{http_client:%s}" % self._http_client
