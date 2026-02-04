#!/bin/sh

which pyinstaller > /dev/null 2>&1
if [ $? != 0 ]; then
    which pipx > /dev/null 2>&1
    if [ $? != 0 ]; then
        echo "Please install pipx with your package manager, and run this script again."
        exit 1
    else
        echo "Installing dependencies..."
        pipx install pyinstaller > /dev/null 2>&1
        pipx ensurepath > /dev/null 2>&1
        echo "Dependencies installed. Please reopen your terminal to refresh your PATH, and run this script again."
        exit 1
    fi
fi
echo "Compiling..."
pyinstaller --onefile dtdl.py > /dev/null 2>&1
if [ $? != 0 ]; then
    echo "PyInstaller error. Aborting."
    exit 1
fi
rm -r build
rm dtdl.spec
echo "Finished compiling!"
exit 0
