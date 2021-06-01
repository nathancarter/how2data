#!/usr/bin/bash

example="How to print a caterpillar"
taskname="How to FILL THIS IN"
taskfolder="database/tasks/$taskname"

cd "$( dirname "${BASH_SOURCE[0]}" )"
mkdir "$taskfolder"

cp "examples/R/$example/description.Rmd"   "$taskfolder/description.md"
cp "examples/R/$example/R.Rmd"             "$taskfolder/R.Rmd"
cp "examples/Python/$example/Python.ipynb" "$taskfolder/Python.ipynb"
