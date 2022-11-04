#!/usr/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"

if [ $# -eq 0 ]
then
  echo "Usage: unite_preview.sh <existing task name>"
  echo "This script moves all source files from the preview folder into the folder "
  echo "specified by the user as the task name.  That parameter is required."
  echo "Compare this to finish_preview.sh, which creates the task folder from scratch,"
  echo "while this command assumes it exists and is just adding to it."
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

if [ ! -e "$FOLDER" ]
then
  echo "No such folder: \"$FOLDER\""
  exit 1
fi

echo ""
echo "> Moving files below to \"$FOLDER\""
ls -1 $SOURCES
mv $SOURCES "$FOLDER"

echo ""
echo "> Removing files below"
ls -1 $GENERATED
rm -rf $GENERATED

