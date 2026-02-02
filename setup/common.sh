#!/usr/bin/env bash

# common include guard
if [[  -n "${COMMON_INCLUDED}" ]]; then
    return
fi

COMMON_INCLUDED=1

declare -A __INCLUDED_SOURCES

# include guard
# directory is from original script not local file directory
include() {
    if [ ! -f "$1" ]; then
        echo "File $1 not found"
        return 1
    fi

    newFile=$(realpath "$1")

    if [[ -z "${__INCLUDED_SOURCES[$newFile]}" ]]; then
        __INCLUDED_SOURCES["$newFile"]=1
        builtin source "$newFile"
    fi
}

confirm_print() {
    printf "\n%b\nPress enter to continue..." "$1"
    read
}

slow_print() {
    echo -e "\n$1"
    sleep 0.5
}

auto_menu() {
    HEIGHT=$((LINES / 2))
    WIDTH=$((COLUMNS / 2))
    MENU_HEIGHT=$((HEIGHT - 10))
    [ $MENU_HEIGHT -lt 4 ] && MENU_HEIGHT=4

    dialog --colors --stdout \
        --title "$1" \
        --menu "$2" \
        $HEIGHT $WIDTH $MENU_HEIGHT \
        "${@:3}"
}

auto_yesno() {
    HEIGHT=$((LINES / 2))
    WIDTH=$((COLUMNS / 2))

    dialog --colors --stdout \
        --title "$1" \
        --yesno "${@:3}" \
        $HEIGHT $WIDTH
}

determine_requirements() {
    if [ ! -d resources/local/vosk-models ]; then
        echo -E "\Z1\ZbRequirements NOT Met\nRequired Download: Vosk Models\Zn"
    elif [ ! -d resources/local/piper-voices ]; then
        echo -E "\Z1\ZbRequirements NOT Met\nRequired Download: Piper Voices\Zn"
    else
        echo -E "\Z2\ZbAll Requirements Met\Zn"
    fi
}
