#!/usr/bin/env python3

import os
import urllib.request
import xml.etree.ElementTree as ET


# class is defined so it can be handled in the main try block
class updateException(Exception):
    pass


# returns if update, current version, latest version
def check_for_updates() -> tuple[bool, str, str]:
    if os.path.exists("tmp"):
        os.system("rm -rf tmp")

    os.mkdir("tmp")

    if not os.path.exists("resources/local/version"):
        with open("resources/local/version", "w") as f:
            f.write("0.0.0")

    with open("resources/local/version", "r") as f:
        curVersion = f.read().strip()

    xml_url = "https://github.com/rienovie/homePotato/releases.atom"

    urllib.request.urlretrieve(xml_url, "tmp/atom.xml")

    tree = ET.parse("tmp/atom.xml")
    root = tree.getroot()

    prefix = "{http://www.w3.org/2005/Atom}"
    versions = []
    # comes with prefix
    for item in root:
        if item.tag == f"{prefix}entry":
            for child in item:
                if child.tag == f"{prefix}title":
                    if child.text is not None and child.text.startswith("Release_"):
                        versions.append(child.text.split("_")[-1])

    versions.sort(reverse=True)

    return versions[0] > curVersion, curVersion, versions[0]


if __name__ == "__main__":
    if not os.path.exists("resources"):
        print("Resources directory not found")
        print("Script must be run from homePotato root directory")
        if (
            input(
                "If you wish to run the script anyway, please type 'yes' and hit enter: "
            )
            != "yes"
        ):
            exit(0)

    update = check_for_updates()

    if not update[0]:
        print("No updates available")
        exit(0)

    print("Update available!")
    print("Current Version: " + update[1] + " -> New Version: " + update[2])

    download_url = (
        "https://github.com/rienovie/homePotato/archive/refs/tags/v"
        + update[2]
        + ".zip"
    )

    urllib.request.urlretrieve(download_url, "tmp/update.zip")
    os.system("unzip tmp/update.zip -d tmp")
    os.remove("tmp/update.zip")
    os.system(f"cp -rf tmp/homePotato-{update[2]}/* .")
    os.system("rm -rf tmp")

    with open("resources/local/version", "w") as f:
        f.write(update[2])

    print("System update complete")

    print("Script complete")
