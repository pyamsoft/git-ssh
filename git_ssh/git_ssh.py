#!/usr/bin/env python3

import os

from .config.config import Config
from .errors.expected import ExpectedError
from .logger.logger import Logger
from .config.read import (ReadConfig, ReadSource)
from .config.remove import (RemoveConfig, RemoveSource)
from .config.write import (WriteConfig, WriteSource)


class GitSsh:
    """Current config version"""
    CONFIG_VERSION = 2

    @staticmethod
    def _abs_path(directory, file):
        """Concats a directory and file path together to an absolute path"""
        return "{}/{}".format(directory, file)

    @staticmethod
    def _version_path(directory, file):
        """Concats a directory and file path together to an absolute path"""
        return "{}/{}.{}".format(directory, file, GitSsh.CONFIG_VERSION)

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

    @staticmethod
    def _parse_create_string(create_string, config_dir):
        if not create_string:
            Logger.d("No create_string passed, empty WriteConfig")
            return WriteConfig.empty()

        split_create = create_string.split(":")
        if len(split_create) != 2:
            raise InvalidCreateStringError(create_string)

        name, key = split_create
        path = GitSsh._version_path(config_dir, name)
        Logger.d("Create string -- name: {}, path: {}, key: {}".format(
            name, path, key))
        return WriteConfig(name, path, WriteSource(key))

    @staticmethod
    def _parse_remove(remove_config, config_dir):
        if not remove_config:
            Logger.d("No remove_config passed, empty RemoveConfig")
            return RemoveConfig.empty()

        path = GitSsh._version_path(config_dir, remove_config)
        Logger.d("Remove config -- name: {}, path: {}".format(
            remove_config, path))
        return RemoveConfig(remove_config, path, RemoveSource(path))

    @staticmethod
    def _list_all_configs(config_dir):
        Logger.log("Listing all configs in: {}\n".format(config_dir))
        counter = 0
        for config_file in os.listdir(config_dir):
            abspath = GitSsh._abs_path(config_dir, config_file)
            if os.path.isfile(abspath):
                read_config = ReadConfig(config_file, abspath,
                                         ReadSource(abspath))

                content = read_config.read()
                if content:
                    counter += 1
                    Logger.log("[{}] ({})".format(config_file, abspath))
                    Logger.log(content)

        Logger.log("Total config count: {}".format(counter))

    def __init__(self, git, wrapper_args, git_args):
        """Initialize GitSsh wrapper"""
        self._git = git
        self._git_args = git_args
        self._ssh = Config.empty()
        self._ssh_options = []
        self._done = False
        self._handle_wrapper_args(wrapper_args)

    def _handle_wrapper_args(self, wrapper_args):
        """Parse the wrapper specific arguments into correct flags"""
        config_dir = self._find_config_dir(wrapper_args.config_dir)

        # Make the config dir
        try:
            os.mkdir(config_dir)
        except FileExistsError as e:
            Logger.e("Unable to create config dir, may already exist")
            Logger.e(e)

        write_config = self._parse_create_string(wrapper_args.create_string,
                                                 config_dir)

        # If this is a valid WriteConfig
        if write_config.name():
            Logger.d("Write key file for {}".format(write_config.name()))
            write_config.write()

        remove_config = self._parse_remove(wrapper_args.remove_config,
                                           config_dir)

        # If this is a valid RemoveConfig
        if remove_config.name():
            Logger.d("Remove config: {}".format(write_config.name()))
            remove_config.remove()

        if wrapper_args.list:
            GitSsh._list_all_configs(config_dir)
            self._done = True
        else:
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
        if self._done:
            Logger.d("Already done, ignore call()")
        else:
            if self._ssh.path():
                self._git.ssh_call(self._git_args, self._ssh,
                                   self._ssh_options)
            else:
                self._git.call(self._git_args)


class NoSshConfigError(ExpectedError):
    def __init__(self, key):
        """No config found for requested name"""
        super(NoSshConfigError, self) \
            .__init__("Could not find config matching key: {}".format(key))


class InvalidCreateStringError(ExpectedError):
    def __init__(self, string):
        """Invalid create string format, either too many args or too little"""
        super(InvalidCreateStringError, self) \
            .__init__("Create string is invalid format: {}".format(string))
