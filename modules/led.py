from __future__ import absolute_import

import time
import logging
import serial
from datetime import datetime

logger = logging.getLogger(__name__)


class Hook:
    def __init__(self):
        self.comm = serial.Serial('/dev/arduino')

    def on_pass(self, data):
        now = datetime.utcnow()
        duration = data['end']['datetime'] - now
        self.prender()
        time.sleep(duration.seconds)
        self.apagar()

    def prender(self):
        self.comm.write('\x01')

    def apagar(self):
        self.comm.write('\x00')
