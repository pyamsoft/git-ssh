#!/usr/bin/env python3

from ..logger.logger import Logger


class WriteConfig:

    def __init__(self, name, path, key):
        """Initialize a WriteConfig object"""
        self._name = name
        self._path = path
        self._key = key

    def write(self):
        """Write the content stream to the source _path

        If the content fails to write, False is returned
        If the content is invalid, a RuntimeError is raised
        """
        if self._key is None:
            raise RuntimeError("Cannot call write() with invalid key")

        if self._path is None:
            raise RuntimeError("Cannot call write() with invalid path")

        if self._name is None:
            raise RuntimeError("Cannot call write() with invalid name")

        try:
            src = open(self._path, mode="w")
        except OSError as e:
            Logger.e("Unable to write {}".format(self._path))
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
                    Logger.log("Config created: {} at {}".format(
                        self._name, self._path))
                    return True
