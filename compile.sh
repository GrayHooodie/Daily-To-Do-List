#!/bin/bash

which pyinstaller > /dev/null 2>&1
if [ $? != 0 ]; then
    echo "You must have PyInstaller installed. If Pip is installed, try 'pipx install pyinstaller', or install pyinstaller with your package manager."
    exit 1
fi
echo "Compiling..."
pyinstaller -F dtdl.py > /dev/null 2>&1
if [ $? != 0 ]; then
    echo "PyInstaller error. Aborting."
    exit 1
fi
rm -r build
rm dtdl.spec
echo "Finished compiling!"