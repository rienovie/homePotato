#!/usr/bin/env bash

# NOTE: this is where if you want to contribute add more languages to be automatically downloaded/handled

submenu_download_vosk() {
    while true; do
        choice=$(auto_menu "homePotato - Downloads - Vosk" "Choose language:" \
            "English" "Default English Small Vosk Model (0.15)" \
            "Manual" "Manually Download Vosk Models" \
            "Back" "Back to Downloads")
        case $choice in
            "English")
		mkdir -p resources/local/vosk-models
		slow_print "Downloading Vosk-Model-Small-en-us-0.15"
		if ! wget -O resources/local/vosk-models/vosk-model-small-en-us-0.15.zip https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip; then
			slow_print "Download failed, please try again."
			return 0
		fi
		slow_print "Download complete"
		unzip resources/local/vosk-models/vosk-model-small-en-us-0.15.zip -d resources/local/vosk-models
		rm resources/local/vosk-models/vosk-model-small-en-us-0.15.zip
		slow_print "Extraction complete"
		confirm_print "Model downloaded and extracted."
		return 0
                ;;
            "Manual")
		mkdir -p resources/local/vosk-models
		slow_print "Follow link and place downloaded models in resources/local/vosk-models"
		confirm_print "https://alphacephei.com/vosk/models"
		slow_print "Script will assume you have downloaded, unziped, and placed models inside directory."
		return 0
                ;;
            "Back" | "")
                return 0
                ;;
        esac
    done
}
