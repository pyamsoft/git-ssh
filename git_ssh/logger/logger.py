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


import sys


class Logger:
    """Static flag controlling whether the logger should output or not"""
    enabled = False

    def __init__(self):
        """Logger is purely a static implementation, no class instances"""
        raise NotImplementedError("No instances of Logger allowed")

    @staticmethod
    def log(message, *args, **kwargs):
        """Log a message to stdout without needing debug mode"""
        print(f"{message}", *args, **kwargs, file=sys.stdout)

    @staticmethod
    def d(message, *args, **kwargs):
        """Log a message to stdout if debug mode is on"""
        if Logger.enabled:
            print(f"DEBUG  {message}", *args, **kwargs, file=sys.stderr)

    @staticmethod
    def e(message, *args, **kwargs):
        """Log an error message to stderr if debug mode is on"""
        if Logger.enabled:
            print(f"ERROR  {message}", *args, **kwargs, file=sys.stderr)

    @staticmethod
    def fatal(message, *args, **kwargs):
        """Log an error message to stderr and exit"""
        print(f"FATAL  {message}", *args, **kwargs, file=sys.stderr)
        sys.exit(1)
