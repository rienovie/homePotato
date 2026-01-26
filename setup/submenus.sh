#!/usr/bin/env bash

include setup/vosk_download.sh
include setup/piper_menu.sh

submenu_download() {
    while true; do
        message=$(determine_requirements)
        choice=$(auto_menu "homePotato - Downloads" "$message" \
            "Vosk" "Download Vosk Models (Speech to Text)" \
            "Piper" "Download Piper Voices (Text to Speech)" \
            "Back" "Back to main menu")

        case $choice in
            "Vosk")
                submenu_download_vosk
                ;;
            "Piper")
                submenu_download_piper
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
            "Vosk" "Vosk Options (Speech to Text)" \
            "Piper" "Piper Options (Text to Speech)" \
            "Back" "Back to main menu")

        case $choice in
            "Vosk")
                confirm_print "Not implemented yet"
                ;;
            "Piper")
                confirm_print "Not implemented yet"
                ;;
            "Back" | "")
                return 0
                ;;
        esac
    done
}
