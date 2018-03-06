#!/usr/bin/env python3

from ..logger.logger import Logger


class ReadConfig:
    @staticmethod
    def from_(config):
        """Create a new ReadConfig from a Config object"""
        return ReadConfig(config.name(), ReadSource(config.path()))

    @staticmethod
    def empty():
        """Returns an empty ReadConfig object

        An empty ReadConfig can be used in the place of None but contains
        invalid data and should not be used as an actual data source.
        """
        return ReadConfig("", EmptyReadSource())

    def __init__(self, name, source):
        """Initialize a ReadConfig object

        For empty Config objects, use the static empty() function
        """
        self._name = name
        self._source = source

    def name(self):
        """Return the name of this config"""
        return self._name

    def read(self):
        """Read content from the ConfigSource and return it to the caller"""
        return self._source.read()


class EmptyReadSource:

    def read(self):
        return ""


class ReadSource:
    def __init__(self, path):
        """Create a new ReadSource object

        Path can be absolute or relative depending on how the caller wishes
        to use the source
        """
        self._path = path

    def read(self):
        """Read all content from the file located at path and return it

        If the path does not point to a valid file, the empty string is returned
        If the path fails to read, an empty string is returned
        """
        try:
            src = open(self._path, mode="r")
        except OSError as e:
            Logger.e("Cannot read content from path: {}".format(self._path))
            Logger.e(e)
            return ""
        else:
            with src:
                content = src.read()
                if content is None:
                    return ""
                else:
                    return content
