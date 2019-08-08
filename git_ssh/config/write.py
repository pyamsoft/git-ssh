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
            Logger.e("Unable to write '{}'".format(self._path))
            Logger.e(e)
            return False
        else:
            with src as s:
                content = """# Created by git-ssh
# You may modify this file, but it may be overwritten without warning by
# git-ssh if you tell it to do so.

Host *
    IdentityFile {}
    IdentitiesOnly yes
    AddKeysToAgent yes

""".format(self._key)
                if not s.write(content):
                    return False
                else:
                    Logger.log("Config created: '{}' at '{}'".format(
                        self._name, self._path
                    ))
                    return True
