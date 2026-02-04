#!/bin/sh

which pyinstaller > /dev/null 2>&1
if [ $? != 0 ]; then
    which pipx > /dev/null 2>&1
    if [ $? != 0 ]; then
        if command -v apt > /dev/null 2>&1; then
            sudo --prompt="Enter password to install python:" apt install pipx
        elif command -v dnf > /dev/null 2>&1; then
            sudo --prompt="Enter password to install python:" dnf install pipx
        elif command -v yum > /dev/null 2>&1; then
            sudo --prompt="Enter password to install python:" yum install pipx
        elif command -v zypper > /dev/null 2>&1; then
            sudo --prompt="Enter password to install python:" zypper install python3-pipx
        elif command -v pacman > /dev/null 2>&1; then
            sudo --prompt="Enter password to install python:" pacman -Syu python-pipx
        else
            echo "Please install pipx with your package manager, and run this script again."
            exit 1
        fi
    fi
    echo "Installing dependencies..."
    pipx install pyinstaller > /dev/null 2>&1
    pipx ensurepath > /dev/null 2>&1
    echo "Dependencies installed. Please reopen your terminal to refresh your PATH variable, and run this script again."
    exit 1
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
