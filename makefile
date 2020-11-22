#!/bin/bash

export REQ_FILE = requirements.txt
export PROJECT_DIR = monkeywrench
export TEST_DIR = tests


#############################################################
#              Commands for Python environment              #
#############################################################

py-init:
	if [[ -d ./venv ]]; then rm -rf venv; fi \
	&& python3.6 -m venv venv \
	&& . venv/bin/activate \
	&& pip install --upgrade pip setuptools wheel \
	&& pip install -r ${REQ_FILE}

requirements:
	if [[ -f ${REQ_FILE} ]]; then rm -f ${REQ_FILE}; fi \
	&& . venv/bin/activate \
	&& pip freeze | grep 'monkeywrench' -v > ${REQ_FILE}


update:
	. venv/bin/activate \
	&& pip install --upgrade pip setuptools wheel


install:
	pip install -e .

#############################################################
#              Commands for testing                         #
#############################################################


lint:
	. venv/bin/activate \
	&& python -m flake8 ${PROJECT_DIR} ${TEST_DIR}

test:
	. venv/bin/activate \
	&& python -m pytest ${TEST_DIR} -p no:warnings -s

qa:
	make test
	make lint


#############################################################
#              Build and Distribution                       #
#############################################################

build:
	. venv/bin/activate \
	&& python setup.py sdist bdist_wheel

release:
  ifdef version
		./bin/release --version $(version)
  else
	  ./bin/release
  endif


#	&& pip freeze | grep 'flake8\|mccabe\|pycodestyle\|zipp\|pyflakes\|importlib-metadata\|toml\|pluggy\|six\|pyparsing\|packaging\|iniconfig\|attrs\|py\|more-itertools\|monkeywrench\|pytest' -v > ${LIB_REQ}
