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


import os

from ..logger.logger import Logger


class RemoveConfig:

    def __init__(self, name, path):
        """Initialize a RemoveConfig object"""
        self._name = name
        self._path = path

    def remove(self):
        """Remove this config"""
        if self._path is None or self._path == "":
            return

        if self._name is None or self._name == "":
            return

        try:
            os.remove(self._path)
        except OSError as err:
            Logger.e("Unable to remove: '{}' at '{}'".format(self._name, self._path))
            Logger.e(err)
        else:
            Logger.log("Config removed: '{}' at '{}'".format(self._name, self._path))
