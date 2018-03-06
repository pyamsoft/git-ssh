#!/usr/bin/env python3


class Config:
    @staticmethod
    def empty():
        """Returns an empty Config object

        An empty Config can be used in the place of None but contains invalid
        data and should not be used as an actual data source.
        """
        return Config("", "")

    def __init__(self, name, path):
        """Initialize a Config object

        For empty Config objects, use the static empty() function
        """
        self._name = name
        self._path = path

    def name(self):
        """Return the name of this config"""
        return self._name

    def path(self):
        """Return the path to this config on the filesystem

        May be absolute or relative depending on how this config was created
        """
        return self._path
