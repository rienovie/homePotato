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
        "Update" "Update homePotato" \
        "Flash OS" "Flash OS to microSD" \
        "Download" "Download voices, models, and other resources" \
        "Options" "Configure homePotato" \
        "Exit" "Exit homePotato setup")

    case $choice in
        "Update")
            if auto_yesno "homePotato Version ($(cat resources/local/version.txt))" --msg "This will call the update script that might overwrite any changes you have made to any files but will NOT touch your configuration files in resources/local (except the version.txt file). Are you sure you wish to continue?"; then
                python setup/update.py
                confirm_print "Update complete"
            fi
            ;;
        "Flash OS")
            submenu_flash_os
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
