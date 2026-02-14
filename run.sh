#!/usr/bin/env bash

# TODO: this script should reject or maybe auto-load the setup script if the system is not setup yet

if [ ! -d "resources" ]; then
	echo "This script must be run from the homePotato root directory"
	exit 1
fi

source bash/activate_env.sh

if [ ! -f resources/local/exit ]; then
	echo "null" > resources/local/exit
fi

# While loop wraps the application so updates and crashes restart the application
while true; do
	value=$(cat resources/local/exit)
	
    if [ $value == "update"  ]; then
		echo "Update called"
		python python/update.py
		echo "null" > resources/local/exit
	elif [ $value == "exit"  ]; then
		echo "Exit called"
		echo "null" > resources/local/exit
		exit 0
	elif [ $value == "null"  ]; then
		echo "exit value is $(cat resources/local/exit)"
		echo "null" > resources/local/exit
	fi

    python3 python/run.py
done
