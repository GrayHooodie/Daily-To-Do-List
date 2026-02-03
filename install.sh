#!/bin/bash

echo "Installing..."
ls ~/.local/bin/ | grep dtdl > /dev/null 2>&1
if [ $? == 0 ]; then
    cp dist/dtdl ~/.local/bin/dtdl
else
    sudo --prompt="Enter password to make program available to all users. Otherwise, type Ctrl+c:" cp dist/dtdl /usr/bin 2> /dev/null
    if [ $? == 1 ]; then
        mkdir -p ~/.local/bin
        echo $PATH | grep ~/.local/bin > /dev/null 2>&1
        if [ $? == 1 ]; then
            if [[ "$(echo $SHELL)" =~ "bash" ]]; then
                echo "export PATH=$PATH:~/.local/bin" >> ~/.bashrc
                source ~/.bashrc
            elif [[ "$(echo $SHELL)" =~ "zsh" ]]; then
                echo "export PATH=$PATH:~/.local/bin" >> ~/.zshrc
                source ~/.zshrc
            elif [[ "$(echo $SHELL)" =~ "fish" ]]; then
                echo "set -U fish_user_paths ~/.local/bin" >> ~/.config/fish/config.fish
            else
                echo "Unknown shell. Aborting."
                exit 1
            fi
        fi
        cp dist/dtdl ~/.local/bin/
    fi
fi

which python3 > /dev/null 2>&1
if [ $? == 0 ]; then
    python3 setup.py
else
    echo "Please install python, then run this script again."
    exit 1
fi

which dtdl > /dev/null 2>&1
if [ $? == 1 ]; then
    echo "Error. Not installed."
else
    echo "Installed to $(which dtdl)"
fi
