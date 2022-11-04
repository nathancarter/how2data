#!/usr/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"

if [ $# -ne 3 ]
then
  echo "Usage: prepare_preview.sh \"<existing task name>\" \"<solution1>\" \"<solution2>\""
  echo "This script moves the description.md file for the given task into the preview folder"
  echo "and converts an existing solution into a new format, ready to be edited for a new"
  echo "software package."
  echo "Example:"
  echo "prepare_preview.sh \"How to do basic mathematical computations\" Python.ipynb Julia.md"
  exit 1
fi

IN_FORMAT="${2##*.}"
if [ "$IN_FORMAT" = "md" ]
then
  IN_FORMAT=markdown
fi
OUT_FORMAT="${3##*.}"
if [ "$OUT_FORMAT" = "md" ]
then
  OUT_FORMAT=markdown
fi

SRC_FOLDER="./database/tasks/$1"
DEST_FOLDER="./preview"

SRC_FILES=$(ls -A "$SRC_FOLDER/$2")
if [ ! "$SRC_FILES" ]
then
  echo "No such source file: \"$SRC_FOLDER/$2\""
  echo "These are the files in that folder:"
  echo "-----------------------------------"
  ls -1 "$SRC_FOLDER"
  exit 1
fi

echo ""
echo "> Copying description.md to \"$DEST_FOLDER\""
cp "$SRC_FOLDER/description.md" "$DEST_FOLDER/description.md"

echo ""
if [ "$IN_FORMAT" = "markdown" ]
then
  if [ "$OUT_FORMAT" = "markdown" ]
  then
    echo "> Copying from: $SRC_FOLDER/$2"
    echo "            to: $DEST_FOLDER/$3"
    cp "$SRC_FOLDER/$2" "$DEST_FOLDER/$3"
  else
    echo "Converting markdown input to non-markdown output not supported by this script."
    exit 1
  fi
else
  echo "> Converting \"$2\" to \"$3\""
  jupyter nbconvert "$SRC_FOLDER/$2" --to=$FORMAT --output-dir="$DEST_FOLDER" --output="$3"
fi

echo ""
echo "> Done."
echo ""
