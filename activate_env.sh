#!/usr/bin/env bash

if [ "$BASH_SOURCE" = "$0" ]; then
	echo "This script must be run with 'source' command!"
	exit 1
fi

if [ -d ".venv" ]; then
	source .venv/bin/activate
	echo "Virtual environment activated"
else
	echo "Did not find .venv directory, creating virtual environment"
	python3.11 -m venv .venv
	source .venv/bin/activate
	echo "Virtual environment created and activated"
	echo "Installing dependencies"
	pip install -r requirements.txt
	echo "Environment setup complete"
fi
