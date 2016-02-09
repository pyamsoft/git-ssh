# git-ssh
An ssh-key selection wrapper for git

## Usage  
### Options
The script currently handles the following option(s):  

--ssh CONFIG

The name identifier of a config file in the ${config_dir}  
The contents expected in the CONFIG file are listed in the CONFIGURATION section  

### Configuration

A valid config file can take any name, with or without spaces, and can  
have any extension, though normal convention is to have none. For any  
config files with spaces in the name, they will need to be properly  
escaped.  

Examples:     rsa    "second key"   github.ssh.key  

A valid config file consists of exactly one line of content: A path  
to an ssh key. While a relative path will work, it is generally recommended  
that one uses absolute paths to be clear as to which key is being requested.  
Comments are not allowed in the config file, in any kind of syntax.  
Any variables in the config file will be interpreted by the shell.  

Examples:  
In example config file <rsa>  
~/.ssh/id_rsa  

In example config file <"second key">  
${HOME}/.ssh/id_dsa  

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

## Limitations

Due to parsing limitations, the --ssh must be the first option specified  
If it is not, we assume it is not requested.  

This is because git has issues with us snatching away the $@ variable, as  
for example assume that we store vars into a temporary variable  
```
${git_options}="status help clone"  
```

Git will fail saying that there is no valid option 'status help clone'  
It will properly handle the status option when using the $@ variable however.  

Unless a work around is found to allow git to parse individual arguments,  
this hard requirement must stay.  

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
