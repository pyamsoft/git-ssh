# git-ssh
An ssh-key selection wrapper for git

## Usage  
### Options
The script currently handles the following option(s):  
```

  --ssh CONFIG

  The name identifier of a config file in the ${config_dir}  
  The contents expected in the CONFIG file are listed in the CONFIGURATION  
  section  

  --ssh-opts COMMA-SEPARATED-OPTIONS

  A comma separated list of options to pass to the invocation of ssh. It is  
  recommended that this list of options be surrounded by double quotes.

  --create-config NAME:PATH

  Create a config called NAME with the path PATH.  
  Does not stop operation following completion  

  --remove-config NAME

  Remove the config specified by NAME.  
  Does not stop operation following completion  

  --list-configs

  Lists the contents of the ${config_dir}  
  Stops operation following completion  

```

### Configuration

Configuration files are just plain ssh_config files that have, by default, a  
couple of options preset. The config files apply by default to all hosts and  
have a specific `IdentityFile` noted. The `IdentitiesOnly` option is on,  
meaning that only the `IdentityFile` specified can be used. One can override  
these settings via the --ssh-args command line option, or by editing the  
generated config file directly.

CONFIG files are by default searched for in `${XDG_CONFIG_HOME}/git-ssh`  

## Usability

To make `git-ssh` more friendly to the `git` user, the following can be performed  
in the shell to allow for shell completion among other nice things:  
```
alias git="/path/to/git-ssh"  
```
This will make all calls to `git` resolve first to `git-ssh` in the interactive  
shell. If you wish to take this a step further, you can create a symlink to  
`git-ssh` in your path before git itself is resolved, and then any program  
which expects `git` will now work with `git-ssh`.  

*Note* that overriding the environment to resolve first to `git-ssh` when calling  
`git` may pose a security risk in unforseen situations. This project does not  
guarantee the safety or stability of the system in the event that the  
environment is overrideen to use `git-ssh` for all git related calls.

If you do not want to replace the normal resolution for a call to `git` you  
can instead call git with the following:  
```
For example, say you wanted to do:

 $ git push -u origin master

You can call the command as follows:

 $ git ssh --ssh github push -u origin master

```

### Usage and Options
```
usage: git-ssh [--ssh CONFIG] [--create-config NAME:SSH_KEY_PATH]
               [--remove-config NAME] [--ssh-opts OPTION STRING]
               [--list-configs] [--git-path PATH] [--ssh-help] [--ssh-version]
               [--ssh-debug]

optional arguments:
  --ssh CONFIG          Name of a config file in the config directory
  --create-config NAME:SSH_KEY_PATH
                        Create a new ssh config using NAME:SSH_KEY_PATH
  --remove-config NAME  Remove an existing config by NAME
  --ssh-opts OPTION STRING
                        Comma separated string of SSH options
  --list-configs        List all configs found in the config directory
  --git-path PATH       Path to Git binary (defaults to /usr/bin/git)
  --ssh-help            Display this help and exit
  --ssh-version         Display the version and exit
  --ssh-debug           Turn on debug logging
```

## Questions

Questions or issues should be either posted in the issue section of this  
repository, or directed by email to pyamsoft @ pyam(dot)soft(at)gmail(dot)com

## Issues

Check the issues page on GitHub for any notes about outstanding or existing  
issues. If you encounter a problem with git-ssh of which no such  
issue already exists please feel free to help the developer by creating an  
issue ticket.

## License

GPLv2

```

  The GPLv2 License

    Copyright (C) 2017  Peter Kenji Yamanaka

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License along
    with this program; if not, write to the Free Software Foundation, Inc.,
    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

```
