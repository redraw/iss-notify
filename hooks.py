from __future__ import absolute_import

import os
import imp
import threading
import logging

logger = logging.getLogger(__name__)


class HookManager:
    def __init__(self):
        self.hooks = set()
        self.dirname = 'modules'

        for filename in os.listdir(self.dirname):
            if filename.endswith('.py'):
                path = os.path.join(self.dirname, filename)
                mod = imp.load_source(filename, path)
                hook = mod.Hook()
                self.hooks.add(hook)

    def trigger(self, event, *args, **kwargs):
        for hook in self.hooks:
            callback = getattr(hook, event, None)
            if callback:
                t = threading.Thread(target=callback, args=args, kwargs=kwargs)
                t.start()
