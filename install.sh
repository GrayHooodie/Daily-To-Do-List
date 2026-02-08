#!/bin/sh

if ! [ -f ./dist/dtdl ]; then
    echo "Please run './compile.sh', then run this script again."
    exit 1
fi

echo "Installing..."
ls ~/.local/bin/ | grep dtdl > /dev/null 2>&1
if [ $? = 0 ]; then
    cp dist/dtdl ~/.local/bin/dtdl
else
    whchpth='U'
    read -p "Would you like to make the program available to all users? (requires superuser, i.e. your password) [y/n]:" whchpth
	whchpth=$(echo $whchpth | tr '[:lower:]' '[:upper:]')
    while [ "$whchpth" != 'Y' ] && [ "$whchpth" != 'N' ]; do 
		read -p "Enter 'y' or 'n': " whchpth
		whchpth=$(echo $whchpth | tr '[:lower:]' '[:upper:]')
	done
    if [ $whchpth = 'Y' ]; then
        sudo cp dist/dtdl /usr/bin 2> /dev/null
    fi
    if [ $? != 0 ] || [ $whchpth = 'N' ]; then
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

which dtdl > /dev/null 2>&1
if [ $? != 0 ]; then
    echo "Error. Is '~/.local/bin' in your PATH variable?"
    exit 1
else
    echo "Installed to $(which dtdl)"
fi
exit 0
