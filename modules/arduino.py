from __future__ import absolute_import

import time
import logging
import serial

logger = logging.getLogger(__name__)


class Hook:
    def __init__(self):
        self.comm = serial.Serial('/dev/arduino')

    def on_pass(self, duration):
        self.prender()
        time.sleep(int(duration))
        self.apagar()
    
    def prender(self):
        self.comm.write('\x01')

    def apagar(self):
        self.comm.write('\x00')
