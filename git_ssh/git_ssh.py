#!/usr/bin/env python3

import os

from .config.config import Config
from .errors.expected import ExpectedError
from .logger.logger import Logger


class GitSsh:
    """Current config version"""
    CONFIG_VERSION = 2

    @staticmethod
    def _abs_path(directory, file):
        """Concats a directory and file path together to an absolute path"""
        return "{}/{}".format(directory, file)

    @staticmethod
    def _is_config(name, file):
        """Check if a given file matches the expected config"""
        return "{}.{}".format(name, GitSsh.CONFIG_VERSION) == file

    @staticmethod
    def _find_ssh_config(config_dir, name):
        """Find the correct Config file given a wanted name and directory"""
        Logger.d("Find SSH config for: {} in {}".format(name, config_dir))
        for config_file in os.listdir(config_dir):
            abspath = GitSsh._abs_path(config_dir, config_file)
            if os.path.isfile(abspath):
                Logger.d("Check config: {}".format(abspath))
                if GitSsh._is_config(name, config_file):
                    Logger.d("Found config: {} at {}".format(name, abspath))
                    return Config(name, abspath)

        return Config.empty()

    @staticmethod
    def _find_config_dir(arg):
        """Find the config directory either from arguments or environment"""
        config_dir = None
        if arg:
            config_dir = arg
            Logger.d("Config dir from argument: {}".format(config_dir))

        # Or from environment
        if not config_dir:
            try:
                xdg_env = os.environ["XDG_CONFIG_HOME"]
                if xdg_env:
                    config_dir = "{}/git-ssh".format(xdg_env)
                    Logger.d("Config dir from XDG_CONFIG_HOME: {}".format(
                        config_dir))
            except KeyError:
                Logger.e("Error getting config dir from XDG_CONFIG_HOME")

                # Set to nothing so it will be handled by next if
                config_dir = None

        # Or from default
        if not config_dir:
            config_dir = os.path.expanduser("~/.config/git-ssh")
            Logger.d("Config dir from fallback: {}".format(config_dir))

        return config_dir

    def __init__(self, git, wrapper_args, git_args):
        """Initialize GitSsh wrapper"""
        self._git = git
        self._git_args = git_args
        self._ssh = Config.empty()
        self._ssh_options = []
        self._handle_wrapper_args(wrapper_args)

    def _handle_wrapper_args(self, wrapper_args):
        """Parse the wrapper specific arguments into correct flags"""
        config_dir = self._find_config_dir(wrapper_args.config_dir)

        # Find ssh config if specified
        name = wrapper_args.ssh
        if name:
            found_config = self._find_ssh_config(config_dir, name)
            if found_config.name():
                self._ssh = found_config
            else:
                raise NoSshConfigError(name)

    def call(self):
        """Call through to either Git or wrap in an SSH environment"""
        if self._ssh.path():
            self._git.ssh_call(self._git_args, self._ssh, self._ssh_options)
        else:
            self._git.call(self._git_args)


class NoSshConfigError(ExpectedError):
    def __init__(self, key):
        """No config found for requested name"""
        super(NoSshConfigError, self) \
            .__init__("Could not find config matching key: {}".format(key))
