#!/usr/bin/env python3

import os

from ..logger.logger import Logger


class RemoveConfig:

    def __init__(self, name, path):
        """Initialize a RemoveConfig object"""
        self._name = name
        self._path = path

    def remove(self):
        """Remove this config"""
        try:
            os.remove(self._path)
        except Exception as e:
            Logger.e(
                "Unable to remove: {} at {}".format(self._name, self._path))
            Logger.e(e)
            return False
        else:
            Logger.log(
                "Config removed: {} at {}".format(self._name, self._path))
            return True
