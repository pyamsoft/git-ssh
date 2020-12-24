# git-ssh
An ssh-key selection wrapper for git


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

CONFIG files are by default searched for in `${XDG_CONFIG_HOME}/git-ssh`

## Example

For example, lets say you have 2 different ssh keys at `$HOME/.ssh`

`id_git_personal` and `id_git_company`

To make git use your personal id for a project, creat it via
```
$ git-ssh create personal $HOME/.ssh/id_git_personal
```

and then use it by eval'ing the output of the `export` command:

```
$ eval "$(git-ssh export personal)"
```

This will load up your environment with the following:
```
export GIT_SSH_COMMAND='ssh -F "$HOME/.config/git-ssh/github.2"'
```

which, when used by `git` will load up ssh with the `IdentityFile` of `id_git_personal`

To switch to your company key when accessing company repositories,
create it and then export it just like you did your personal. It's that simple!

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
