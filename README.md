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

  --ssh-args COMMA-SEPARATED-OPTIONS

  A comma separated list of options to pass to the invocation of ssh. It is  
  recommended that this list of options be surrounded by double quotes.

  --config-dir DIR

  The path to the directory where configs are stored.

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
have a specific IdentityFile noted. The IdentitiesOnly option is on, meaning  
that only the IdentityFile specified can be used. One can override these  
settings via the --ssh-args command line option.

CONFIG files are by default searched for in the
${config_dir} location, which defaults to
$XDG_CONFIG_HOME/git-ssh. This directory is not created by default.

## Usability

To make git-ssh more friendly to the git user, the following can be performed  
in the shell to allow for shell completion among other nice things:  
```
alias git="/path/to/git-ssh"  
```
This will make all calls to git resolve first to git-ssh in the interactive  
shell. If you wish to take this a step further, you can create a symlink to  
git-ssh in your path before git itself is resolved, and then any program  
which expects git will now work with git-ssh.  

Note that overriding the environment to resolve first to git-ssh when calling  
git may pose a security risk in unforseen situations. This project does not  
guarantee the safety or stability of the system in the event that the  
environment is overrideen to use git-ssh for all git related calls

## Nested Quotes

The script runs an eval call on all of the arguments passed in because the author  
is bad and does not know how to shell script properly. Unfortunately, until he  
can learn properly, it is what it is. If you are, for example, commiting from the  
command line and your commit message includes nested quotations, you will need to  
include not one, not two, but three backslashes to escape your nested quotes.  

Sorry.

## Questions

Questions or issues should be either posted in the issue section of this  
repository, or directed by email to pyamsoft @ pyam(dot)soft(at)gmail(dot)com

## Issues

Check the issues page on GitHub for any notes about outstanding or existing  
issues. If you encounter a problem with git-ssh of which no such  
issue already exists please feel free to help the developer by creating an  
issue ticket.

## License

MIT  

```

  The MIT License (MIT)

  Copyright (c) 2016 Peter Kenji Yamanaka

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
  SOFTWARE.

```
