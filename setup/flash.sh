#!/usr/bin/env bash

include setup/common.sh

# Before flashing, verify all requirements are met

submenu_flash() {
    HEIGHT=$((LINES / 2))
    WIDTH=$((COLUMNS / 2))

    dialog --msgbox "Current configuration:
    $(cat setup/flash_options)
    " $HEIGHT $WIDTH

    while true; do
        sdCard=$(grep "sdCard=" setup/flash_options | awk -F '=' '{print $2}')
        msg="\Z1\ZbYou are about to erase all data and flash $sdCard!\n\nThis cannot be undone!\n\nPlease confirm!\Zn"

        if dialog --colors --title "homePotato - Flash" --yes-label "Yes flash $sdCard" --no-label "Cancel" --yesno "$msg" $((LINES / 2)) $((COLUMNS / 2)); then
            flash_os
            return 0
        else
            return 0
        fi

    done
}

flash_os() {

    if [ -f resources/local/img/*.img.xz ]; then
        slow_print "Found OS image"
    elif [ $(grep "image=" setup/flash_options | awk -F '=' '{print $2}') = "Default"  ]; then
        slow_print "Downloading default OS image"
        if [ $(grep "device=" setup/flash_options | awk -F '=' '{print $2}') = "AML-S905X-CC" ]; then
            # NOTE: This is the default image for the lePotato board any changes would be here
            wget -P resources/local/img/ https://dl.armbian.com/lepotato/Noble_current_minimal
        else
            confirm_print "Please place downloaded disk image '.img.xz' file in resources/local/img directory before flashing"
            return 1
        fi
    fi
    image=$(find resources/local/img -type f -name "*.img.xz")
    slow_print "Flashing OS"
    xz -dc "$image" | sudo dd of="$sdCard" bs=1M status=progress
    slow_print "OS flashed, copying git repo to $sdCard"
    mkdir -p tmp
    # so we can mount the partition
    sdCard+="p1"
    sudo mount "$sdCard" tmp
    sudo mkdir tmp/homePotato
    sudo rsync -av \
        --exclude resources/local/img \
        --exclude .git \
        --exclude .gitignore \
        --exclude tmp \
        --exclude .venv \
        --exclude __pycache__ \
        . tmp/homePotato
    sudo umount tmp
    rmdir tmp
    slow_print "Local git repo copied to $sdCard/homePotato"
    slow_print "Any changes made to this repo will NOT be reflected on the flashed OS"
    slow_print "Log in on the device and run setup.sh in the homePotato directory"
    slow_print "You'll have to install python3.11, and git for full functionality and setup"
    confirm_print "Have fun!"
}

