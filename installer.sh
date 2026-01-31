#!/bin/bash

echo "Creating virtual environment..."
python3 -m venv env > /dev/null 2>&1
source env/bin/activate > /dev/null 2>&1
echo "Installing dependencies..."
python3 -m pip install -r requirements.txt > /dev/null 2>&1
echo "Compiling..."
env/bin/pyinstaller -F dtdl.py > /dev/null 2>&1
echo "Installing..."
which dtdl > /dev/null 2>&1
if [ $? == 0 ]
then
    if [ $(which dtdl) == ~/.local/bin/dtdl ]
    then
        mv dist/dtdl ~/.local/bin/dtdl
    fi
fi
ls dist | grep dtdl > /dev/null 2>&1
if [ $? == 0 ]
then
    sudo --prompt="Enter password to make program available to all users. Otherwise, type Ctrl+c:" mv dist/dtdl /usr/bin 2> /dev/null
    if [ $? == 1 ]
    then
        ls ~/.local/bin > /dev/null 2>&1
        if [ $? == 2 ]
        then
            mkdir ~/.local/bin
        fi
        echo $PATH | grep ~/.local/bin > /dev/null 2>&1
        if [ $? == 1 ]
        then
            if [ $(echo $0) == bash ]
            then
                echo "export PATH=$PATH:~/.local/bin" >> ~/.bashrc
            elif [ $(echo $0) == zsh ]
            then
                echo "export PATH=$PATH:~/.local/bin" >> ~/.zshrc
            else
                echo "set -x PATH $PATH:~/.local/bin" >> ~/.config/fish/config.fish
            fi
        fi
        mv dist/dtdl ~/.local/bin/
    fi
fi
ls dist | grep dtdl > /dev/null 2>&1
if [ $? == 0 ]
then
    echo "Error. Not installed."
    exit
fi
rmdir dist
rm -r build
rm dtdl.spec

which dtdl > /dev/null 2>&1
if [ $? == 1 ]
then
    echo "Error. Not installed."
else
    echo "Installed to $(which dtdl)"
fi