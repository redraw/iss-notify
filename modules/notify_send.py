"""
To make this module work, make sure DBUS_SESSION_BUS_ADDRESS environment variable is set up

Run this in the shell,
[/path/to/iss-notify]$ env | grep DBUS >> .env
"""
import os
import sys
import logging
import subprocess


logger = logging.getLogger(__name__)


class Hook:

    def on_pass(self, data):
        duration = data['end']['datetime'] - data['start']['datetime']

        cmd = [
            'notify-send',
            '-t', str(duration.seconds),
            '-i', 'preferences-desktop-screensaver',
            'ISS above!',
            'Highest point at %s %s' % (data['highest']['az'], data['highest']['alt'])
        ]

        #logger.info(dict(os.environ))

        logger.info(cmd)
        subprocess.call(cmd)

