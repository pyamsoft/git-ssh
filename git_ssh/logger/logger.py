#!/usr/bin/env python3

import sys


class Logger:
    """Static flag controlling whether the logger should output or not"""
    enabled = False

    def __init__(self):
        """Logger is purely a static implementation, no class instances"""
        raise NotImplementedError("No instances of Logger allowed")

    @staticmethod
    def log(message, *args):
        """Log a message to stdout without needing debug mode"""
        if args:
            print("{}".format(message), args, file=sys.stdout)
        else:
            print("{}".format(message), file=sys.stdout)

    @staticmethod
    def d(message, *args):
        """Log a message to stdout if debug mode is on"""
        if Logger.enabled:
            if args:
                print("DEBUG  {}".format(message), args, file=sys.stderr)
            else:
                print("DEBUG  {}".format(message), file=sys.stderr)

    @staticmethod
    def e(message, *args):
        """Log an error message to stderr if debug mode is on"""
        if Logger.enabled:
            if args:
                print("ERROR  {}".format(message), args, file=sys.stderr)
            else:
                print("ERROR  {}".format(message), file=sys.stderr)

    @staticmethod
    def fatal(message, *args):
        """Log an error message to stderr and exit"""
        if args:
            print("FATAL  {}".format(message), args, file=sys.stderr)
        else:
            print("FATAL  {}".format(message), file=sys.stderr)
        sys.exit(1)
