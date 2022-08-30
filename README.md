# git-ssh
An ssh-key selection wrapper for git

### Why

This exists because SSH keys and git are a little weird when it comes to
working together. Let's say you work at home on personal projects, and at
a company for work-related projects. These two project environments should
be completely seperated due to personal or work requirements, and so they
include different SSH keys owned by different accounts on your favorite
centralized Git hosting service. You sometimes work on personal code, and
then need to context switch over to work code. You go to git pull your latest
work repository changes and get hit with this:

```
ERROR: Repository not found.
fatal: Could not read from remote repository.

Please make sure you have the correct access rights
and the repository exists.
```

This is because you are using git with the wrong SSH key, so you are blocked
from seeing or pushing to a private ssh secure repository.

You can solve this problem by creating a git config file and configuring it to use
a specific SSH key when you are interacting with a specific website, say only using
`id_work.rsa` when accessing `github.com`, but now you've hit a different problem,
which is that your personal repositories hosted on the same website are now not
accessible because your work SSH key is different from your personal SSH key.

You feel balder by the minute. Enter `git-ssh`, a very simple shell script to help
you keep your remaining hair on your head.

## Example

For example, lets say you have 2 different ssh keys at `$HOME/.ssh`

`id_git_personal` and `id_git_company`

To make git use your personal id for a project, creat it via
```sh
$ git-ssh create personal $HOME/.ssh/id_git_personal
```

and then use it by eval'ing the output of the `export` command:

```
$ eval "$(git-ssh export personal)"
```

This will load up your environment with the following:
```sh
export GIT_SSH_COMMAND='ssh -F "$HOME/.config/git-ssh/personal.2"'
```

which, when used by `git` will load up ssh with the `IdentityFile` of `id_git_personal`

To switch to your company key when accessing company repositories,
create it and then export it just like you did your personal. It's that simple!

```sh
$ git-ssh create work $HOME/.ssh/id_git_company
$ eval "$(git-ssh export work)"
```

#### Some more fun

`git` has a fun feature in certain environments where, if a program on your `$PATH`
starts with `git-*`, like `git-ssh`, you can call it as `git ssh` on the CLI.

This allows it to feel like just another `git` subcommand, and works with all
of the `git-ssh` commands:

```sh
$ git ssh create test ~/.ssh/id_my_test.rsa
$ git ssh export test
export GIT_SSH_COMMAND='ssh -F "$HOME/.config/git-ssh/test.2"'
$ eval "$(git ssh export test)"
```

### Usage and Options
```
usage: git-ssh

[Commands]
export <config>           Load a config from CONFIG_DIR to TARGET_CONFIG
list                      List all configs in CONFIG_DIR
create <config> <path>    Create a new <config> pointing to file name <path>
delete <config>           Delete a <config>
help                      This help
```

### Configuration

Configuration files are just plain ssh_config files that have, by default, a
couple of options preset. The config files apply by default to all hosts and
have a specific `IdentityFile` noted. The `IdentitiesOnly` option is on,
meaning that only the `IdentityFile` specified can be used. One can override
these settings by editing the generated config file directly.

NOTE: If you edit the config file, it may be over-written by a future `major`
version update to `git-ssh`

CONFIG files are by default searched for in `${XDG_CONFIG_HOME}/git-ssh`

## Issues

Check the issues page on GitHub for any notes about outstanding or existing
issues. If you encounter a problem with git-ssh of which no such
issue already exists please feel free to help the developer by creating an
issue ticket.

## License

GPLv2

```
  Copyright (C) 2020  Peter Kenji Yamanaka

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

```
