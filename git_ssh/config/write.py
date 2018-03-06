#!/usr/bin/env python3

from ..logger.logger import Logger


class WriteConfig:
    @staticmethod
    def from_(config):
        """Create a new RemoveConfig from a Config object"""
        return WriteConfig(config.name(), config.path(),
                           WriteSource(config.path()))

    @staticmethod
    def empty():
        """Returns an empty WriteConfig object

        An empty WriteConfig can be used in the place of None but contains
        invalid data and should not be used as an actual data source.
        """
        return WriteConfig("", "", EmptyWriteSource())

    def __init__(self, name, path, source):
        """Initialize a WriteConfig object

        For empty Config objects, use the static empty() function
        """
        self._name = name
        self._path = path
        self._source = source

    def name(self):
        """Return the name of this config"""
        return self._name

    def write(self):
        """Write the content to the WriteSource"""
        return self._source.write(self._name, self._path)


class EmptyWriteSource:
    def write(self, name, path):
        return False


class WriteSource:
    def __init__(self, key):
        """Create a new WriteSource object

        Path can be absolute or relative depending on how the caller wishes
        to use the source
        """
        self._key = key

    def write(self, name, path):
        """Write the content stream to the source _path

        If the content fails to write, False is returned
        If the content is invalid, a RuntimeError is raised
        """
        if not self._key:
            raise RuntimeError("Cannot call write() with invalid key")

        if not path:
            raise RuntimeError("Cannot call write() with invalid path")

        if not name:
            raise RuntimeError("Cannot call write() with invalid name")

        try:
            src = open(path, mode="w")
        except OSError as e:
            Logger.e("Unable to write {}".format(path))
            Logger.e(e)
            return False
        else:
            with src:
                content = """# Created by git-ssh
# You may modify this file, but it may be overwritten without warning by
# git-ssh if you tell it to do so.

Host *
    IdentityFile {}
    IdentitiesOnly yes
    AddKeysToAgent yes

""".format(self._key)
                result = src.write(content)
                if result is None:
                    return False
                else:

                    Logger.log("Config created: {} at {}".format(name, path))
                    return True
