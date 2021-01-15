"""
Created on 23 Dec 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import json

from abc import abstractmethod

from scs_core.comms.uds_client import UDSClient


# --------------------------------------------------------------------------------------------------------------------

class GasInferenceClient(object):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, uds_client: UDSClient):
        """
        Constructor
        """
        self._uds_client = uds_client                       # UDSClient


    # ----------------------------------------------------------------------------------------------------------------

    def wait_for_server(self):
        self._uds_client.open()

        self._uds_client.request(json.dumps(None))
        self._uds_client.wait_for_response()

        self._uds_client.log('connected')


    def open(self):
        self._uds_client.open()


    def close(self):
        self._uds_client.close()


    @abstractmethod
    def infer(self, gas_sample, board_temp):
        pass