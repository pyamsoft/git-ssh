#!/usr/bin/env python3

import os

from .constants import PathConstants
from .config.config import Config
from .errors.expected import ExpectedError
from .logger.logger import Logger
from .config.read import ReadConfig
from .config.remove import RemoveConfig
from .config.write import WriteConfig


class GitSsh:
    """Current config version"""
    CONFIG_VERSION = 2
    XDG_CONFIG = "XDG_CONFIG_HOME"

    @staticmethod
    def _abs_path(directory, file):
        """Concats a directory and file path together to an absolute path"""
        return f"{directory}/{file}"

    @staticmethod
    def _version_path(directory, file):
        """Concats a directory and file path together to an absolute path"""
        return f"{directory}/{file}.{GitSsh.CONFIG_VERSION}"

    @staticmethod
    def _is_config(name, file):
        """Check if a given file matches the expected config"""
        return f"{name}.{GitSsh.CONFIG_VERSION}" == file

    @staticmethod
    def _find_ssh_config(config_dir, name):
        """Find the correct Config file given a wanted name and directory"""
        Logger.d(f"Find SSH config for: {name} in {config_dir}")
        for config_file in os.listdir(config_dir):
            abspath = GitSsh._abs_path(config_dir, config_file)
            if os.path.isfile(abspath):
                Logger.d(f"Check config: {abspath}")
                if GitSsh._is_config(name, config_file):
                    Logger.d(f"Found config: {name} at {abspath}")
                    return Config(name, abspath)

        return Config.empty()

    @staticmethod
    def _find_config_dir():
        """Find the config directory either from arguments or environment"""
        config_dir = None
        try:
            xdg_env = os.environ[GitSsh.XDG_CONFIG]
            if xdg_env:
                config_dir = f"{xdg_env}/git-ssh"
                Logger.d(f"Config dir from {GitSsh.XDG_CONFIG}: {config_dir}")
        except KeyError:
            Logger.e(f"Error getting config dir from {GitSsh.XDG_CONFIG}")

            # Set to nothing so it will be handled by next if
            config_dir = None

        # Or from default
        if not config_dir:
            config_dir = os.path.expanduser(PathConstants.DEFAULT_CONFIG_DIR)
            Logger.d(f"Config dir from fallback: {config_dir}")

        return config_dir

    @staticmethod
    def _parse_create_string(create_string, config_dir):
        if not create_string:
            Logger.d("No create_string passed, empty WriteConfig")
            return WriteConfig("", "", "")

        split_create = create_string.split(":")
        if len(split_create) != 2:
            raise InvalidCreateStringError(create_string)

        name, key = split_create
        path = GitSsh._version_path(config_dir, name)
        Logger.d(f"Create string -- name: {name}, path: {path}, key: {key}")
        return WriteConfig(name, path, key)

    @staticmethod
    def _parse_remove(remove_config, config_dir):
        if not remove_config:
            Logger.d("No remove_config passed, empty RemoveConfig")
            return RemoveConfig("", "")

        path = GitSsh._version_path(config_dir, remove_config)
        Logger.d(f"Remove config -- name: {remove_config}, path: {path}")
        return RemoveConfig(remove_config, path)

    @staticmethod
    def _list_all_configs(config_dir):
        Logger.log(f"Listing all configs in: {config_dir}\n")
        counter = 0
        for config_file in os.listdir(config_dir):
            abspath = GitSsh._abs_path(config_dir, config_file)
            if os.path.isfile(abspath) and \
                    abspath.endswith(str(GitSsh.CONFIG_VERSION)):
                read_config = ReadConfig(abspath)
                counter += 1
                Logger.log(f"[{config_file}] ({abspath})")

                Logger.log("")
                for line in read_config.read():
                    Logger.log("    ", line, end="")
                Logger.log("")

        Logger.log(f"Total config count: {counter}")

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
        config_dir = self._find_config_dir()

        # Make the config dir
        try:
            os.mkdir(config_dir)
        except FileExistsError as e:
            Logger.e("Unable to create config dir, may already exist")
            Logger.e(e)

        write_config = self._parse_create_string(wrapper_args.create_string,
                                                 config_dir)

        # If the write config is empty, this does nothing
        write_config.write()

        remove_config = self._parse_remove(wrapper_args.remove_config,
                                           config_dir)

        # If the remove_config is empty, this does nothing
        remove_config.remove()

        # Parse ssh options into list
        if wrapper_args.ssh_opts:
            for option in wrapper_args.ssh_opts.split(","):
                self._ssh_options.append(f"-o {option} ")

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
            .__init__(f"Could not find config matching key: {key}")


class InvalidCreateStringError(ExpectedError):
    def __init__(self, string):
        """Invalid create string format, either too many args or too little"""
        super(InvalidCreateStringError, self) \
            .__init__(f"Create string is invalid format: {string}")
