#!/usr/bin/env python3

from ..logger.logger import Logger


class ReadConfig:

    def __init__(self, path):
        """Initialize a ReadConfig object"""
        self._path = path

    def read(self):
        """Read all content from the file located at path and return it

        If the path does not point to a valid file, an empty string is returned
        If the path fails to read, an empty string is returned
        """
        if self._path is None:
            raise RuntimeError("Cannot call read() with invalid path")

        try:
            src = open(self._path, mode="r")
        except OSError as e:
            Logger.e(f"Cannot read content from path: '{self._path}'")
            Logger.e(e)
            yield ""
        else:
            with src:
                line = src.readline()
                while line:
                    yield line
                    line = src.readline()
