#!/bin/sh

echo "Installing..."
ls ~/.local/bin/ | grep dtdl > /dev/null 2>&1
if [ $? = 0 ]; then
    cp dist/dtdl ~/.local/bin/dtdl
else
    sudo --prompt="Enter password to make program available to all users. Otherwise, type Ctrl+c:" cp dist/dtdl /usr/bin 2> /dev/null
    if [ $? != 0 ]; then
        mkdir -p ~/.local/bin
        echo $PATH | grep ~/.local/bin > /dev/null 2>&1
        if [ $? != 0 ]; then
            if [ $(echo $SHELL | grep -oE '(\w+)$') = "bash" ]; then
                echo "export PATH=$PATH:~/.local/bin" >> ~/.bashrc
                source ~/.bashrc
            elif [ $(echo $SHELL | grep -oE '(\w+)$') = "zsh" ]; then
                echo "export PATH=$PATH:~/.local/bin" >> ~/.zshrc
                source ~/.zshrc
            elif [ $(echo $SHELL | grep -oE '(\w+)$') = "fish" ]; then
                echo "set -U fish_user_paths ~/.local/bin" >> ~/.config/fish/config.fish
            else
                echo "Please add '~/.local/bin' to your PATH variable, and run this script again."
                exit 1
            fi
        fi
        cp dist/dtdl ~/.local/bin/
    fi
fi

which python3 > /dev/null 2>&1
if [ $? != 0 ]; then
    echo "Installing python..."
    if command -v apt > /dev/null 2>&1; then
        sudo --prompt="Enter password to install python:" apt install python3 > /dev/null 2>&1
    elif command -v dnf > /dev/null 2>&1; then
        sudo --prompt="Enter password to install python:" dnf install python3 > /dev/null 2>&1
    elif command -v yum > /dev/null 2>&1; then
        sudo --prompt="Enter password to install python:" yum install python3 > /dev/null 2>&1
    elif command -v zypper > /dev/null 2>&1; then
        sudo --prompt="Enter password to install python:" zypper install python3 > /dev/null 2>&1
    elif command -v pacman > /dev/null 2>&1; then
        sudo --prompt="Enter password to install python:" pacman -Syu python3 > /dev/null 2>&1
    else
        echo "Please install python with your package manager, and run this script again."
        exit 1
    fi
fi
if [ $? != 0 ]; then
    echo "Python must be installed for program setup."
    exit 1
python3 setup.py

which dtdl > /dev/null 2>&1
if [ $? != 0 ]; then
    echo "Error. Is '~/.local/bin' in your PATH variable?"
    exit 1
else
    echo "Installed to $(which dtdl)"
fi
exit 0
