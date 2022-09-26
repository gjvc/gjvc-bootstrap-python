#! /usr/bin/env make

# GNU make --------------------------------------------------------------------

.SHELLFLAGS 	:= -eu -o pipefail -c
SHELL       	:= /bin/bash
MAKEFLAGS   	+= --no-builtin-rules
MAKEFLAGS   	+= --warn-undefined-variables


# paths -----------------------------------------------------------------------

this-file       := $(abspath $(firstword $(MAKEFILE_LIST)))
this-file-dir   := $(dir $(this-file))
ROOT            := $(this-file-dir:/=)


# variables -------------------------------------------------------------------

ifeq ($(origin PYTHON), undefined)
	base_python_default := $(shell command -v python3)
else
	base_python_default := $(PYTHON)
endif

base_python_default 		?= $(shell command -v python)
base_python             	:= $(realpath $(base_python_default))
base_python_implementation	:= $(shell $(base_python) -c 'import platform; print( f"{platform.python_implementation().lower()}" )')
base_python_version     	:= $(shell $(base_python) -c 'import platform; print( f"{platform.python_version_tuple()[ 0 ]}.{platform.python_version_tuple()[ 1 ]}" )')

venv_root                   := $(ROOT)/.venv
venv_python                 := $(venv_root)/bin/python
                            
requirement_txt             := $(ROOT)/etc/pip/requirement.txt
requirement_txt_version     := $(requirement_txt).$(base_python_implementation).$(base_python_version)
                            
pip_install_options_base    := --isolated --upgrade
pip_install_options_ssl     := --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org
pip_install_options         := $(pip_install_options_base) $(pip_install_options_ssl)


# targets ---------------------------------------------------------------------

default : $(venv_root) $(requirement_txt_version)

clean :
	rm -rf $(venv_root)
	rm -rf $(requirement_txt_version)


# rules -----------------------------------------------------------------------

.PHONY : $(requirement_txt_version) $(requirement_txt)

$(venv_root) :
	rm -rf $(venv_root)
	$(base_python) -m venv $(venv_root)

$(requirement_txt_version) : $(requirement_txt) $(venv_root)
	$(venv_python) -m pip install $(pip_install_options) pip setuptools wheel
	$(venv_python) -m pip install $(pip_install_options) --requirement $(<)
	$(venv_python) -m pip check
	$(venv_python) -m pip freeze | sort | sed '/pkg_resources==0.0.0/d' > $(@)

