#!/usr/bin/env python3

import os
import sys
import xml.etree.ElementTree as ET
# import urllib.request


if not os.path.exists("resources"):
    print("Script must be run from homePotato root directory")
    sys.exit(1)

# if not os.path.exists("tmp"):
#     os.mkdir("tmp")
# if os.path.exists("tmp/atom.xml"):
#     os.remove("tmp/atom.xml")

with open("resources/local/version.txt", "r") as f:
    curVersion = f.read().strip()

print("Current Version: " + curVersion)

xml_url = "https://github.com/rienovie/homePotato/releases.atom"

# urllib.request.urlretrieve(xml_url, "tmp/atom.xml")
tree = ET.parse("tmp/atom.xml")
root = tree.getroot()

# comes with prefix
for item in root:
    item.tag = item.tag.removeprefix("{http://www.w3.org/2005/Atom}")
    print(item.tag)


print("Script complete")
