#!/bin/sh

DESTDIR="${DESTDIR:-/}"
PREFIX="${PREFIX:-/usr/local}"

installer()
{
  printf -- 'Installing...\n'

  # Set umask to permissive
  umask 022

  # Prepare directories
  mkdir -p "${DESTDIR}/etc/git-ssh/install" || return 1

  # Install using python
  python3 setup.py install \
    --record="${DESTDIR}/etc/git-ssh/install/files.txt" \
    --root="${DESTDIR}" \
    --prefix="${PREFIX}" \
    --optimize=1 || return 1

  # Install documentation
  install -m 644 -D README.md "${DESTDIR}/${PREFIX}/share/doc/git-ssh" || return 1

  # Install license
  install -m 644 -D LICENSE "${DESTDIR}/${PREFIX}/share/licenses/git-ssh" || return 1

  # Install bash completion
  install -m 644 -D res/shell/bash/bash_completion "${DESTDIR}/usr/share/bash-completion/completions/git-ssh" || return 1
}

uninstaller()
{
  printf -- 'Uninstalling...\n'

  # Set umask to permissive
  umask 022

  # If pip knows about the package, it can uninstall it.
  if pip3 show git_ssh > /dev/null; then
    pip3 uninstall -y git_ssh || return 1
  else
    printf -- 'pip cannot find git_ssh, installed to a non standard location?\n'
    install_history="${DESTDIR}/etc/git-ssh/install/files.txt"
    if [ -e "${install_history}" ] && [ -r "${install_history}" ]; then
      # We can uninstall files manually
      while read -r file; do
        rm -f "${DESTDIR}/${file}" || return 1
      done < "${install_history}"
    else
      printf -- 'Cannot find list of installed files?\n'
      return 1
    fi
  fi

  # Remove configuration directory
  rm -r -f "${DESTDIR}/etc/git-ssh" || return 1

  # Remove license and directory
  rm -r -f "${DESTDIR}/${PREFIX}/share/licenses/git-ssh" || return 1

  # Remove docs
  rm -r -f "${DESTDIR}/${PREFIX}/share/doc/git-ssh" || return 1

  # Remove bash completion
  rm -f "${DESTDIR}/usr/share/bash-completion/completions/git-ssh" || return 1
}

if [ "$(id -u)" -ne 0 ]; then
  echo "You must be root"
  exit 1
fi

if [ ! -e ./git_ssh ]; then
  echo "Must run from git_ssh root directory"
  exit 1
fi

if [ "$1" = "install" ]; then
  installer || exit 1
elif [ "$1" = "uninstall" ]; then
  uninstaller || exit 1
else
  printf -- '%s\n' "$(cat << EOF
  commands:
    install
    uninstall
EOF
)"
fi

exit 0
