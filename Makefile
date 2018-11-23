# The GPLv2 License
#
#   Copyright (C) 2017  Peter Kenji Yamanaka
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License along
#   with this program; if not, write to the Free Software Foundation, Inc.,
#   51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

NAME?=git-ssh
# Really expects to be at /usr
PREFIX?=/usr
MAKEFLAGS:= $(MAKEFLAGS) --no-print-directory

SCRIPT_INSTALL_SRC="git_ssh"
DOC_INSTALL_SRC="README.md"
LICENSE_INSTALL_SRC="LICENSE"
COMPLETION_INSTALL_SRC="res/shell/bash/bash_completion"

DOC_INSTALL_TARGET="$(DESTDIR)/$(PREFIX)/share/doc/$(NAME)/README.md"
LICENSE_INSTALL_TARGET="$(DESTDIR)/$(PREFIX)/share/doc/$(NAME)/LICENSE"
COMPLETION_INSTALL_TARGET="$(DESTDIR)/$(PREFIX)/share/bash-completion/completions/$(NAME)"

.PHONY: all install uninstall

all:
	@echo "Targets"
	@echo " install uninstall"
	@echo $(TARGET)

install:
	@echo "Installing..."
	@./install.sh install

uninstall:
	@echo "Uninstalling..."
	@./install.sh uninstall
