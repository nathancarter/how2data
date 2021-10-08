#!/usr/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"

if [ $# -eq 0 ]
then
  echo "Usage: finish_preview.sh <new task name>"
  echo "This script moves all source files from the preview folder into the folder "
  echo "specified by the user as the new task name.  That parameter is required."
  exit 1
fi

FOLDER="./database/tasks/$@/"
SOURCES="./preview/*.*"
GENERATED="./preview/generated/*"

if [ ! "$(ls -A $GENERATED)" ]
then
  echo "Error: preview has not been run; this folder is empty: $GENERATED"
  exit 1
fi

echo ""
echo "> Making folder \"$FOLDER\"" 
mkdir "$FOLDER"

echo ""
echo "> Moving files below to \"$FOLDER\""
ls -1 $SOURCES
mv $SOURCES "$FOLDER"

echo ""
echo "> Removing files below"
ls -1 $GENERATED
rm -rf $GENERATED

