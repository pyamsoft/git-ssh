#!/usr/bin/env python3

import os
import sh
import sys

from .errors.expected import ExpectedError
from .logger.logger import Logger


class Git:
    """The env var for specifying an SSH command for Git"""
    SSH_COMMAND = "GIT_SSH_COMMAND"

    @staticmethod
    def _handle_git_exception_output(err):
        """Handle the unique exit codes that git may output

        When calling git without any arguments, it will print out its help
        text and actually return 1 instead of a success code of 0.

        When this happens, the 'sh' library prints out this long bunch of
        garbage, when we really just want to print out Git's help text.

        We eat the error stream in certain cases to make the Git output
        through the wrapper stay 1 to 1 with actual Git.
        """
        output = []
        if err.stdout:
            # Git exits with 1 even when just displaying help
            output.append(err.stdout.decode("utf-8"))

        if err.stdout and err.stderr:
            output.append("\n")

        if err.stderr:
            # But it may also handle an actual error
            output.append(err.stderr.decode("utf-8"))

        if output:
            print("".join(output), end="", file=sys.stdout)

    def __init__(self, git_path):
        """Initialize a wrapper for the real Git binary"""
        if not os.path.exists(git_path):
            raise GitError(git_path)
        else:
            self._git_path = git_path

    def call(self, args):
        """A normal call to the git binary, pass arguments through"""
        Logger.d("Calling normal git without ssh wrapped environment")
        Logger.d(f"Git path: {self._git_path} {args}")
        try:
            call_git = sh.Command(self._git_path)
            call_git(args, _fg=True, _tty_in=True, _tty_out=False)
        except sh.ErrorReturnCode as e:
            Logger.e(e)
            self._handle_git_exception_output(e)

    def ssh_call(self, git_args, ssh_config, ssh_args):
        """An ssh wrapped call to the Git binary, set up for specific SSH"""
        if not ssh_config.name() or not ssh_config.path():
            raise BadConfigError(ssh_config)

        Logger.d(f"Calling git with ssh wrapped environment: "
                 f"{ssh_config.name()}")
        Logger.d(f"Git path: {self._git_path} {git_args}")

        ssh_env = os.environ.copy()
        args = "".join(ssh_args)
        ssh_env[Git.SSH_COMMAND] = f"ssh -F '{ssh_config.path()}' {args} "

        Logger.d(f"SSH env: {ssh_env[Git.SSH_COMMAND]}")

        try:
            call_git = sh.Command(self._git_path)
            call_git(
                git_args, _env=ssh_env, _fg=True, _tty_in=True, _tty_out=False)
        except sh.ErrorReturnCode as e:
            Logger.e(e)
            self._handle_git_exception_output(e)


class GitError(ExpectedError):
    def __init__(self, path):
        """Git not found"""
        super(GitError, self) \
            .__init__(f"Git binary cannot be found at: {path}")


class BadConfigError(ExpectedError):
    def __init__(self, config):
        """Invalid config, either name or path is bad"""
        super(BadConfigError, self) \
            .__init__(f"Config is invalid: [name: {config.name()}, "
                      f"path: {config.path()}]")
