#!/usr/bin/env python3
#
#  The GPLv2 License
#
#    Copyright (C) 2019  Peter Kenji Yamanaka
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


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
