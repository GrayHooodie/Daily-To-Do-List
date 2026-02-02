#!/bin/bash

echo "Installing..."
if [ $(which dtdl) == ~/.local/bin/dtdl ]
then
    cp dist/dtdl ~/.local/bin/dtdl
else
    sudo --prompt="Enter password to make program available to all users. Otherwise, type Ctrl+c:" cp dist/dtdl /usr/bin 2> /dev/null
    if [ $? == 1 ]
    then
        mkdir -p ~/.local/bin
        echo $PATH | grep ~/.local/bin > /dev/null 2>&1
        if [ $? == 1 ]
        then
            if [[ "$(echo $SHELL)" =~ "bash" ]]
            then
                echo "export PATH=$PATH:~/.local/bin" >> ~/.bashrc
                source ~/.bashrc
            elif [[ "$(echo $SHELL)" =~ "zsh" ]]
            then
                echo "export PATH=$PATH:~/.local/bin" >> ~/.zshrc
                source ~/.zshrc
            elif [[ "$(echo $SHELL)" =~ "fish" ]]
            then
                echo "set -U fish_user_paths ~/.local/bin" >> ~/.config/fish/config.fish
            else
                echo "Unknown shell. Aborting."
                exit
            fi
        fi
        cp dist/dtdl ~/.local/bin/
    fi
fi

python3 setup.py

which dtdl > /dev/null 2>&1
if [ $? == 1 ]
then
    echo "Error. Not installed."
else
    echo "Installed to $(which dtdl)"
fi