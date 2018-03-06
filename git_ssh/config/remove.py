#!/usr/bin/env python3

import os

from ..logger.logger import Logger


class RemoveConfig:
    @staticmethod
    def empty():
        """Returns an empty RemoveConfig object

        An empty RemoveConfig can be used in the place of None but contains
        invalid data and should not be used as an actual data source.
        """
        return RemoveConfig(EmptyRemoveSource())

    def __init__(self, source):
        """Initialize a RemoveConfig object

        For empty Config objects, use the static empty() function
        """
        self._source = source

    def remove(self):
        """Remove this config"""
        return self._source.remove()


class EmptyRemoveSource:
    def remove(self):
        Logger.d("EmptyRemoveSource.remove() is a no-op")
        return False


class RemoveSource:
    def __init__(self, name, path):
        """Create a new RemoveSource object

        Path can be absolute or relative depending on how the caller wishes
        to use the source
        """
        self._name = name
        self._path = path

    def remove(self, name):
        """Remove the file location at _path from the filesystem

        If the path does not point to a valid file, False is returned
        If the os fails to remove the path, False is returned
        """
        if not self._path:
            raise RuntimeError("Cannot call remove() with invalid path")

        if not name:
            raise RuntimeError("Cannot call remove() with invalid name")

        try:
            os.remove(self._path)
        except Exception as e:
            Logger.e("Unable to remove {}".format(self._path))
            Logger.e(e)
            return False
        else:
            Logger.log("Config removed: {} at {}".format(
                self._name, self._path))
            return True
