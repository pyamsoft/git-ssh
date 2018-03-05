#!/usr/bin/env python3

import argparse
import sh

VERSION = "2.0.0"
CONFIG_VERSION = 2
GIT_BINARY = "/usr/bin/git"


def TODO(message=""):
    raise NotImplementedError("TODO {}".format(message))


class Config:
    def name():
        raise NotImplementedError()

    def path():
        raise NotImplementedError()


class CreateConfig(Config):
    def __init__(self, name, path):
        self._name = name
        self._path = path

    def name():
        return self._name

    def path():
        return self._path


CreateConfig.EMPTY = CreateConfig("", "")


class RemoveConfig(Config):
    def __init__(self, name, path):
        self._name = name
        self._path = path

    def name():
        return self._name

    def path():
        return self._path


RemoveConfig.EMPTY = RemoveConfig("", "")


class Main:
    def __init__(self):
        self._git_args = []
        self._git_ssh_path = ""
        self._remove_config = RemoveConfig.EMPTY
        self._create_config = CreateConfig.EMPTY

    def _create_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--ssh",
            action="store",
            dest="ssh",
            help="Name identified of a config file in the ${config_dir}")
        return parser

    def _handle_git_exception_output(self, err):
        if e.stdout:
            # Git exits with 1 even when just displaying help
            stream = e.stdout
        else:
            # But it may also handle an actual error
            stream = e.stderr
        print(stream.decode("utf-8"), end="")

    def _plain_git_call(self, plain_args):
        try:
            print(sh_git(plain_args))
        except Exception as err:
            self._handle_git_exception_output(err)

    def main(self):
        sh_git = sh.Command(GIT_BINARY)
        wrapper_args, plain_args = self._create_parser().parse_known_args()
        if wrapper_args.ssh is None:
            self._plain_git_call(sh_git, plain_args)
        else:
            TODO()


if __name__ == "__main__":
    Main().main()
