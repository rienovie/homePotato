#!/usr/bin/env bash

include setup/vosk_download.sh
include setup/piper_menu.sh
include setup/configure_flash.sh
include setup/flash.sh

submenu_download() {
    while true; do
        message=$(determine_requirements)
        choice=$(auto_menu "homePotato - Downloads" "$message" \
            "Vosk" "Download Vosk Models (Speech to Text)" \
            "Piper" "Download Piper Voices (Text to Speech)" \
            "Prequisites" "Downloads for post-flash system" \
            "Back" "Back to main menu")

        case $choice in
            "Vosk")
                submenu_download_vosk
                ;;
            "Piper")
                submenu_download_piper
                ;;
            "Prequisites")
                submenu_download_post
                ;;
            "Back" | "")
                return 0
                ;;
        esac
    done
}

submenu_options() {
    while true; do
        choice=$(auto_menu "homePotato - Options" "Choose an option:" \
            "Vosk" "(Speech to Text)" \
            "Piper" "(Text to Speech)" \
            "Weather" "Weather Options" \
            "Back" "Back to main menu")

        case $choice in
            "Vosk")
                confirm_print "Not implemented yet"
                ;;
            "Piper")
                confirm_print "Not implemented yet"
                ;;
            "Weather")
                confirm_print "Not implemented yet"
                ;;
            "Back" | "")
                return 0
                ;;
        esac
    done
}

submenu_flash_os() {
    while true; do
        choice=$(auto_menu "homePotato - Flash" "Choose an option:" \
            "Configure" "Configure options prior to flashing" \
            "Flash" "Flash OS to microSD" \
            "Back" "Back to main menu")

        case $choice in
            "Configure")
                submenu_configure_flash
                ;;
            "Flash")
                submenu_flash
                ;;
            "Back" | "")
                return 0
                ;;
        esac
    done
}

submenu_download_post() {
        while true; do
        choice=$(auto_menu "homePotato - Downloads - Post-Flash" "Run first commands before the prerequisites:" \
            "Update" "apt get update" \
            "Upgrade" "apt get upgrade" \
            "Prequisites" "Run after above commands" \
            "Back" "Back to main menu")

        case $choice in
            "Update")
                sudo apt update || confirm_print "Failed to update"
                confirm_print "Updated"
                ;;
            "Upgrade")
                sudo apt upgrade || confirm_print "Failed to upgrade"
                confirm_print "Upgraded"
                ;;
            "Prequisites")
                # Required for python3.11-dev and python3.11-venv
                # NOTE: if there is any other ppa's to add, add them here
                sudo apt install software-properties-common || confirm_print "Failed to install software-properties-common" && continue
                sudo add-apt-repository ppa:deadsnakes/ppa || confirm_print "Failed to add deadsnakes/ppa" && continue

                # NOTE: still working on this, there will be more added later
                sudo apt install \
                    build-essential \
                    git \
                    libasound2-dev \
                    libpulse-dev \
                    python3-pip \
                    python3-pyaudio \
                    python3.11-dev \
                    python3.11-venv \
                    portaudio19-dev
                confirm_print "Installed required packages"
                ;;
            "Back" | "")
                return 0
                ;;
        esac
    done
}
