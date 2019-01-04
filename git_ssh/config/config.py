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
