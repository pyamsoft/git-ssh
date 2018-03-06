#!/usr/bin/env python3

from ..logger.logger import Logger


class WriteConfig:
    @staticmethod
    def from_(config):
        """Create a new RemoveConfig from a Config object"""
        return WriteConfig(config.name(), WriteSource(config.path()))

    @staticmethod
    def empty():
        """Returns an empty WriteConfig object

        An empty WriteConfig can be used in the place of None but contains
        invalid data and should not be used as an actual data source.
        """
        return WriteConfig("", "")

    def __init__(self, name, source):
        """Initialize a WriteConfig object

        For empty Config objects, use the static empty() function
        """
        self._name = name
        self._source = source

    def name(self):
        """Return the name of this config"""
        return self._name

    def write(self, content):
        """Write the content to the WriteSource"""
        return self._source.write(content)


class WriteSource:
    def __init__(self, path):
        """Create a new WriteSource object

        Path can be absolute or relative depending on how the caller wishes
        to use the source
        """
        self._path = path

    def write(self, content):
        """Write the content stream to the source _path

        If the content fails to write, False is returned
        If the content is invalid, a RuntimeError is raised
        """
        if not content:
            raise RuntimeError("Cannot call write() with invalid content")

        try:
            src = open(self._path, mode="w")
        except OSError as e:
            Logger.e("Unable to write {}".format(self._path))
            Logger.e(e)
            return False
        else:
            with src:
                result = src.write(content)
                if result is None:
                    return False
                else:
                    return True
