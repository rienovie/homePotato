#!/usr/bin/env bash

source common.sh

submenu_download_piper() {
    while true; do
        choice=$(auto_menu "homePotato - Downloads - Piper" "Choose an Option:" \
            "Default" "Download en_US-libritts_r-medium" \
            "List" "List all available voices and choose one" \
            "Back" "Back to Downloads")
        case $choice in
            "Default")
                mkdir -p resources/local/piper-voices
                slow_print "Downloading en_US-libritts_r-medium"
                python -m piper.download_voices en_US-libritts_r-medium --data-dir resources/local/piper-voices
                confirm_print "Download complete"
                return 0
                ;;
            "List")
                mkdir -p resources/local/piper-voices
                slow_print "Getting list of available voices"

                menu_items=()
                voices=$(python -m piper.download_voices)
                if [ -z "$voices" ]; then
                    confirm_print "Error while getting list of voices"
                    return 1
                fi
                while IFS= read -r voice; do
                    menu_items+=("$voice" "")
                done <<< "$voices"

                selected_voice=$(auto_menu "homePotato - Downloads - Piper - List" \
                    "Choose a voice:" \
                    "Back" "" \
                    "${menu_items[@]}" \
                    "Back" "")

                if [ -z "$selected_voice" ] || [ "$selected_voice" = "Back" ]; then
                    continue
                fi

                slow_print "Downloading $selected_voice"
                python -m piper.download_voices "$selected_voice" --data-dir resources/local/piper-voices
                confirm_print "Download complete"
                return 0
                ;;
            "Back")
                return 0
                ;;
        esac
    done
}
