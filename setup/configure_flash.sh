#!/usr/bin/env bash

include setup/common.sh

submenu_configure_flash() {
    while true; do
        choice=$(auto_menu "homePotato - Flash - Configure" "Select 'manual' in device for unsupported boards" \
            "Device" "Choose board (lePotato, Raspberry Pi, etc.)" \
            "Image" "Disk Image to flash" \
            "SD Card" "Choose SD card to flash" \
            "Back" "Back to previous menu")

        case $choice in
            "Device")
                sm_f_cf_device
                ;;
            "Image")
                sm_f_cf_image
                ;;
            "SD Card")
                sm_f_cf_sdCard
                ;;
            "Back" | "")
                return 0
                ;;
        esac
    done
}

sm_f_cf_device() {
    while true; do
        curDevice=$(grep "device=" setup/flash_options | awk -F '=' '{print $2}')
        choice=$(auto_menu "homePotato - Flash - Configure - Device" "Currect Device: $curDevice" \
            "lePotato" "AML-S905X-CC (Default)" \
            "Manual" "Unlisted/Unsupported Device" \
            "Back" "Back to previous menu")

        case $choice in
            "lePotato")
                sed -i 's/^device=.*/device=AML-S905X-CC/' "setup/flash_options"
                mkdir -p resources/local/img
                ;;
            "Manual")
                sed -i 's/^device=.*/device=Manual/' "setup/flash_options"
                mkdir -p resources/local/img
                confirm_print "Please place downloaded disk image '.img.xz' file in resources/local/img directory"
                ;;
            "Back" | "")
                return 0
                ;;
        esac
    done
}

sm_f_cf_image() {
    while true; do
        curImage=$(grep "image=" setup/flash_options | awk -F '=' '{print $2}')
        choice=$(auto_menu "homePotato - Flash - Configure - Image" "Current Image: $curImage" \
            "Default" "Ubuntu 22.04 LTS" \
            "Manual" "Populate setup with downloaded image file" \
            "Back" "Back to previous menu")

        case $choice in
            "Default")
                sed -i 's/^image=.*/image=Default/' "setup/flash_options"
                ;;
            "Manual")
                if [ ! -f resources/local/img/*.img.xz ]; then
                    confirm_print "Disk image file not found in resources/local/img directory"
                else
                    sed -i 's/^image=.*/image=$(realpath resources/local/img/*.img.xz)/' "setup/flash_options"
                fi
                ;;
            "Back" | "")
                return 0
                ;;
        esac
    done
}

sm_f_cf_sdCard() {
    while true; do
        curSdCard=$(grep "sdCard=" setup/flash_options | awk -F '=' '{print $2}')

        menu_items=()
        while read -r name size model; do
            label="$size $model"
            menu_items+=("$name" "$label")
        done < <(lsblk -dn -o NAME,SIZE,MODEL,MOUNTPOINT)

        selected_device=$(auto_menu "homePotato - Flash - Configure - SD Card" "Current Flash Target: $curSdCard" \
            "${menu_items[@]}" \
            "Back" "Back to previous menu")

        if [ -z "$selected_device" ] || [ "$selected_device" = "Back" ]; then
            return 0
        fi

        device_path="/dev/$selected_device"

        sed -i "s|^sdCard=.*|sdCard=$device_path|" setup/flash_options

    done
}
