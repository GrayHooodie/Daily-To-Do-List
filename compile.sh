#!/bin/sh

which pyinstaller > /dev/null 2>&1
if [ $? != 0 ]; then
    which pipx > /dev/null 2>&1
    if [ $? != 0 ]; then
        echo "Installing pipx..."
        if command -v apt > /dev/null 2>&1; then
            sudo --prompt="Enter password to install pipx (needed for dependencies):" apt install pipx -y > /dev/null 2>&1
        elif command -v dnf > /dev/null 2>&1; then
            sudo --prompt="Enter password to install pipx (needed for dependencies):" dnf install pipx -y > /dev/null 2>&1
        elif command -v yum > /dev/null 2>&1; then
            sudo --prompt="Enter password to install pipx (needed for dependencies):" yum install pipx -y > /dev/null 2>&1
        elif command -v zypper > /dev/null 2>&1; then
            sudo --prompt="Enter password to install pipx (needed for dependencies):" zypper install python3-pipx -y > /dev/null 2>&1
        elif command -v pacman > /dev/null 2>&1; then
            sudo --prompt="Enter password to install pipx (needed for dependencies):" pacman -Syu python-pipx -y > /dev/null 2>&1
        else
            echo "Please install pipx with your package manager, and run this script again."
            exit 1
        fi
        which pipx > /dev/null 2>&1 
        if [ $? != 0 ]; then
            echo "Pipx must be installed for dependencies while compiling. Either install pipx, or switch to the main branch where the program is pre-compiled."
            exit 1
        else
            echo "Pipx installed!"
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
