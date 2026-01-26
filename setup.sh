#!/usr/bin/env bash

if [ ! -d resources ]; then
    echo "Please run this script from the homePotato directory"
    exit 1
fi

# setup script files
source setup/common.sh
# NOTE: DO NOT SOURCE ANYTHING ELSE, JUST INCLUDE

include setup/vosk_download.sh
include setup/submenus.sh


# Create resources/local if it doesn't exist
mkdir -p resources/local

slow_print "Welcome to homePotato setup!"
slow_print "This is a work-in-progress and has NOT been released yet!"
confirm_print

while true; do
    message=$(determine_requirements)

    choice=$(auto_menu "HomePotato - Main Setup" "$message" \
        "Update" "Update homePotato from git repo" \
        "Download" "Download voices, models, and other resources" \
        "Options" "Configure homePotato" \
        "Exit" "Exit homePotato setup")

    case $choice in
        "Update")
            curScriptHash=$(sha256sum "setup.sh" | awk '{print $1}')
            slow_print "Updating homePotato from git repo..."
            if ! git pull; then
                slow_print "Git pull failed, unable to update homePotato"
                continue
            fi
            newScriptHash=$(sha256sum "setup.sh" | awk '{print $1}')
            if [ "$curScriptHash" != "$newScriptHash" ]; then
                confirm_print "HomePotato updated and script has changed, restarting setup script..."
                exec ./setup.sh
            else
                confirm_print "HomePotato updated."
            fi
            ;;
        "Download")
            submenu_download
            ;;
        "Options")
            submenu_options
            ;;
        "Exit" | "")
            slow_print "Exiting setup"
            exit 0
            ;;
    esac

done
