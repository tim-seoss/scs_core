#!/usr/bin/env python3

"""
Created on 14 Aug 2020

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import os

from scs_core.comms.uds_server import UDSServer
from scs_core.sys.logging import Logging


# --------------------------------------------------------------------------------------------------------------------
# resources...

# logging...
Logging.config(__name__, verbose=True, exclusive=True)

# server...
location = os.getcwd()
path = os.path.join(location, 'lambda-model.uds')

server = UDSServer(path)
print(server)


# --------------------------------------------------------------------------------------------------------------------
# run...

try:
    server.start()
    print(server)

    for message in server.requests():
        print('request: %s' % message)

        server.respond(message)

except KeyboardInterrupt:
    print()

finally:
    server.stop()
