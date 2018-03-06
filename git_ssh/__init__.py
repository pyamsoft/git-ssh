#!/usr/bin/env python3

import argparse
import sys

from .errors.expected import ExpectedError
from .git_ssh import GitSsh
from .git import Git
from .logger.logger import Logger


class PathConstants:
    """The default path to the real git binary"""
    GIT_PATH = "/usr/bin/git"


def _initialize_parser():
    """Set up the option parser with the options we handle"""
    parser = argparse.ArgumentParser(prog="git-ssh", add_help=False)

    parser.add_argument(
        "--ssh",
        action="store",
        dest="ssh",
        metavar="CONFIG",
        help="Name identified of a config file in the ${config_dir}")
    parser.add_argument(
        "--config-dir",
        action="store",
        dest="config_dir",
        metavar="DIRECTORY",
        help="Directory to store and search for config files")
    parser.add_argument(
        "--git-path",
        action="store",
        dest="git_path",
        metavar="PATH",
        help="Path to Git binary (defaults to {})".format(
            PathConstants.GIT_PATH))
    parser.add_argument(
        "--ssh-help",
        action="store_const",
        const=True,
        dest="help",
        help="Display this help")
    parser.add_argument(
        "--ssh-debug",
        action="store_const",
        const=True,
        dest="debug",
        help="Turn on debug logging")
    return parser


def _parse_options():
    """Parse all possible options

    Options that are specifically handled by git-ssh will go into wrapper_args
    Any normal git options go into plain_args
    """
    parser = _initialize_parser()

    # Parse known args only so we don't error on plain arguments
    wrapper_args, plain_args = parser.parse_known_args()

    # Turn on debugging before we continue if needed
    if wrapper_args.debug:
        Logger.enabled = True

    # Log arguments if debugging
    Logger.d("wrapper args: ", wrapper_args)
    Logger.d("plain args: ", plain_args)

    # Find git path if passed, else default to DEFAULT_GIT_PATH
    git_path = wrapper_args.git_path
    if not git_path:
        git_path = "/usr/bin/git"

    return parser.print_help, git_path, wrapper_args, plain_args


def main():
    """git-ssh a simple wrapper for Git to help with multiple SSH keys"""
    # Parse the options before starting setup
    print_help, git_path, wrapper_args, plain_args = _parse_options()

    # Print out help and exit
    if wrapper_args.help:
        print_help()
        sys.exit(0)

    try:
        wrapper = GitSsh(Git(git_path), wrapper_args, plain_args)
        wrapper.call()
    except ExpectedError as e:
        Logger.fatal(e)