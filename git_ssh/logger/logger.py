#!/usr/bin/env python3

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
