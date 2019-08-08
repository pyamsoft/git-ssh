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
import subprocess
import sys

from .errors.expected import ExpectedError
from .logger.logger import Logger


class Git:
    """The env var for specifying an SSH command for Git"""
    SSH_COMMAND = "GIT_SSH_COMMAND"

    def __init__(self, git_path):
        """Initialize a wrapper for the real Git binary"""
        if not os.path.exists(git_path):
            raise GitError(git_path)
        else:
            self._git_path = git_path

    @staticmethod
    def _run(args, env=None):
        """Call subprocess command"""
        try:
            if hasattr(subprocess, "run"):
                Logger.d("subprocess.run exists, using it")
                subprocess.run(
                    args,
                    env=env,
                    stdin=sys.stdin,
                    stdout=sys.stdout.buffer,
                    stderr=sys.stderr.buffer
                )
            else:
                Logger.d("subprocess.run does not exist, fallback to call")
                subprocess.call(
                    args,
                    env=env,
                    stdin=sys.stdin,
                    stdout=sys.stdout.buffer,
                    stderr=sys.stderr.buffer
                )
        except KeyboardInterrupt as e:
            Logger.e("KeyboardInterrupt triggered, stopping _run")
            Logger.e(e)

    def call(self, args):
        """A normal call to the git binary, pass arguments through"""
        Logger.d("Calling normal git without ssh wrapped environment")
        Logger.d("Git path: {} {}".format(self._git_path, args))

        full_args = [self._git_path]
        if args:
            full_args += args
        self._run(full_args)

    def ssh_call(self, git_args, ssh_config, ssh_args):
        """An ssh wrapped call to the Git binary, set up for specific SSH"""
        if not ssh_config.name() or not ssh_config.path():
            raise BadConfigError(ssh_config)

        Logger.d("Calling git with ssh wrapped environment: {}".format(
            ssh_config.name()
        ))
        Logger.d("Git path: {} {}".format(self._git_path, git_args))

        ssh_env = os.environ.copy()
        args = "".join(ssh_args)
        ssh_env[Git.SSH_COMMAND] = "ssh -F '{}' {} ".format(
            ssh_config.path(), args
        )

        Logger.d("SSH env: {}".format(ssh_env[Git.SSH_COMMAND]))

        full_args = [self._git_path]
        if git_args:
            full_args += git_args
        self._run(full_args, ssh_env)


class GitError(ExpectedError):
    def __init__(self, path):
        """Git not found"""
        super(GitError, self) \
            .__init__("Git binary cannot be found at: {}".format(path))


class BadConfigError(ExpectedError):
    def __init__(self, config):
        """Invalid config, either name or path is bad"""
        super(BadConfigError, self) \
            .__init__(
            "Config is invalid: [name: {}, path: {}]".format(
                config.name(), config.path()
            ))
