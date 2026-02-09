#!/usr/bin/env bash

# NOTE: used to create a release of homePotato

if [ ! -d resources ]; then
    echo "Please run this script from the homePotato directory"
    exit 1
fi

mkdir -p resources/local/release

source setup/common.sh

if git status --porcelain; then
    slow_print "Git repo has uncommitted changes"
    slow_print "Please commit before creating a release"
    exit 1
fi

read -p "Enter Release Version: " version

if [ -d "resources/local/release/$version" ]; then
    slow_print "Release $version already exists"
    exit 1
fi

slow_print "Creating release $version"

mkdir -p "resources/local/release/$version/src"

rsync -av \
    --exclude resources/local \
    --exclude .git \
    --exclude .gitignore \
    --exclude tmp \
    --exclude .venv \
    --exclude __pycache__ \
    . resources/local/release/$version/src


cd resources/local/release/$version/src

zip -r "../homePotato-$version.zip" .
