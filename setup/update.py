#!/usr/bin/env python3

import os
import xml.etree.ElementTree as ET
import urllib.request


if not os.path.exists("resources"):
    print("Resources directory not found")
    print("Script must be run from homePotato root directory")
    if input("If you wish to run the script anyway, please type 'yes' and hit enter: ") != "yes":
        exit(0)

if not os.path.exists("tmp"):
    os.mkdir("tmp")
else:
    os.system("rm -rf tmp")
    os.mkdir("tmp")

if not os.path.exists("resources/local/version.txt"):
    with open("resources/local/version.txt", "w") as f:
        f.write("0.0.0")

with open("resources/local/version.txt", "r") as f:
    curVersion = f.read().strip()

print("Current Version: " + curVersion)

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

if versions[0] <= curVersion:
    print("System is up to date")
    exit(0)

print("Update available!")
print("Current Version: " + curVersion + " -> New Version: " + versions[0])

download_url = "https://github.com/rienovie/homePotato/archive/refs/tags/v" + versions[0] + ".zip"

urllib.request.urlretrieve(download_url, "tmp/update.zip")
os.system("unzip tmp/update.zip -d tmp")
os.remove("tmp/update.zip")
os.system(f"cp -rf tmp/homePotato-{versions[0]}/* .")
os.system("rm -rf tmp")

with open("resources/local/version.txt", "w") as f:
    f.write(versions[0])

print("System update complete")

print("Script complete")
