#!/usr/bin/env python3

#  Copyright (C) 2020  Peter Kenji Yamanaka
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

import os

from .constants import Const
from .config.config import Config
from .errors.expected import ExpectedError
from .logger.logger import Logger
from .config.read import ReadConfig
from .config.remove import RemoveConfig
from .config.write import WriteConfig


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
    def _find_config_dir():
        """Find the config directory either from arguments or environment"""
        config_dir = None
        try:
            xdg_env = os.environ[Const.XDG_CONFIG]
            if xdg_env:
                config_dir = "{}/git-ssh".format(xdg_env)
                Logger.d("Config dir: {}: {}".format(
                    Const.XDG_CONFIG, config_dir
                ))
        except KeyError:
            Logger.e(
                "Error getting config dir from {}".format(Const.XDG_CONFIG)
            )

            # Set to nothing so it will be handled by next if
            config_dir = None

        # Or from default
        if not config_dir:
            config_dir = os.path.expanduser(Const.CONFIG_DIR)
            Logger.d("Config dir from fallback: {}".format(config_dir))

        return config_dir

    @staticmethod
    def _parse_create_string(create_string, config_dir):
        if not create_string:
            Logger.d("No create_string passed, empty WriteConfig")
            return WriteConfig("", "", "")

        split_create = create_string.split(":")
        if len(split_create) != 2:
            raise InvalidCreateStringError(create_string)

        key, name = split_create

        # TODO Validate that key exists at path

        path = GitSsh._version_path(config_dir, name)
        Logger.d("Create string -- name: {}, path: {}, key: {}".format(
            name, path, key
        ))
        return WriteConfig(name, path, key)

    @staticmethod
    def _parse_remove(remove_config, config_dir):
        if not remove_config:
            Logger.d("No remove_config passed, empty RemoveConfig")
            return RemoveConfig("", "")

        found_config = GitSsh._find_ssh_config(config_dir, remove_config)
        if found_config.name():
            path = GitSsh._version_path(config_dir, remove_config)
            Logger.d("Remove config -- name: {}, path: {}".format(
                remove_config, path
            ))
            return RemoveConfig(remove_config, path)

        raise NoSshConfigError(remove_config)

    @staticmethod
    def _list_all_configs(config_dir):
        Logger.log("Listing all configs in: {}\n".format(config_dir))
        counter = 0
        for config_file in os.listdir(config_dir):
            abspath = GitSsh._abs_path(config_dir, config_file)
            if os.path.isfile(abspath) and \
                    abspath.endswith(str(GitSsh.CONFIG_VERSION)):
                read_config = ReadConfig(abspath)
                counter += 1
                Logger.log("[{}] ({})".format(config_file, abspath))

                Logger.log("")
                for line in read_config.read():
                    Logger.log("    ", line, end="")
                Logger.log("")

        Logger.log("Total config count: {}".format(counter))

    def __init__(self, git):
        """Initialize GitSsh wrapper"""
        self._git = git
        self._ssh = Config.empty()
        self._ssh_options = []

    def _generate_ssh_alias(self, alias):
        """Generate an alias for the git command using the wrapper"""
        Logger.d("Generating SSH alias for: {}, use with eval\n".format(alias))

        # If there are options, add them too
        options = ""
        if self._ssh_options:
            options = " ".join(self._ssh_options)
            Logger.d("Adding ssh options to alias: {}".format(options))

        git_path = self._git.path()
        Logger.d("Git found at {} for alias.".format(git_path))

        command = "alias git='git ssh --ssh={} --ssh-git=\"{}\" {}'"
        Logger.log(command.format(alias, git_path, options))

    def _execute_options(self, wrapper_args, config_dir):
        """Parse the wrapper specific arguments and execute commands where possible"""
        if wrapper_args.create_string:
            # If the write config is empty, this does nothing
            GitSsh._parse_create_string(wrapper_args.create_string,
                                        config_dir).write()
            return True

        if wrapper_args.remove_config:
            # If the remove_config is empty, this does nothing
            GitSsh._parse_remove(wrapper_args.remove_config,
                                 config_dir).remove()
            return True

        if wrapper_args.list:
            GitSsh._list_all_configs(config_dir)
            return True

        if wrapper_args.ssh_alias:
            name = wrapper_args.ssh_alias
            if name:
                found_config = GitSsh._find_ssh_config(config_dir, name)
                if found_config.name():
                    self._generate_ssh_alias(name)
                    return True

                raise NoSshConfigError(name)
        else:
            # Find ssh config if specified
            name = wrapper_args.ssh
            if name:
                found_config = GitSsh._find_ssh_config(config_dir, name)
                if found_config.name():
                    self._ssh = found_config
                else:
                    raise NoSshConfigError(name)

        return False

    def handle_options(self, wrapper_args):
        """Parse the wrapper specific arguments into correct flags"""

        config_dir = GitSsh._find_config_dir()

        # Make the config dir
        try:
            os.mkdir(config_dir)
        except FileExistsError as err:
            Logger.e("Unable to create config dir, may already exist")
            Logger.e(err)

        # Parse ssh options into list
        if wrapper_args.ssh_opts:
            for option in wrapper_args.ssh_opts.split(","):
                self._ssh_options.append("-o {} ".format(option))

        done = self._execute_options(wrapper_args, config_dir)
        return GitRunner(self._ssh, self._ssh_options, self._git, done)


class GitRunner:
    """Runs git commands, or if a command has already 'finished' do nothing"""

    def __init__(self, ssh, ssh_options, git, done):
        self._ssh = ssh
        self._ssh_options = ssh_options
        self._git = git
        self._done = done

    def call(self, git_args):
        """Call through to either Git or wrap in an SSH environment"""
        if self._done:
            Logger.d("Already done, ignore call()")
        else:
            if self._ssh.path():
                self._git.ssh_call(git_args, self._ssh, self._ssh_options)
            else:
                self._git.call(git_args)


class NoSshConfigError(ExpectedError):
    """Error when no SSH config can be found for the given name"""

    def __init__(self, key):
        """No config found for requested name"""
        super(NoSshConfigError, self) \
            .__init__("Could not find config matching key: {}".format(key))


class InvalidCreateStringError(ExpectedError):
    """SSH create strings must be passed as PATH_TO_KEY:NAME"""

    def __init__(self, string):
        """Invalid create string format, either too many args or too little"""
        super(InvalidCreateStringError, self) \
            .__init__("""
Create string is invalid format: {}
Create string must be in the format <path to key>:<name>
""".format(string))
