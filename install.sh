#!/bin/sh

if ! [ -f ./dist/dtdl ]; then
    echo "Please run './compile.sh', then run this script again."
    exit 1
fi

echo "Installing..."
copied=0
which dtdl > /dev/null 2>&1
if [ $? = 0 ]; then
	updt='U'
	if [ $(which dtdl | grep '^/home') ]; then
		read -p "Another version of dtdl is detected at '$(which dtdl)'. Would you like to update it? [y/n]: " updt
	elif [ $(which dtdl | grep '^/usr') ]; then
		read -p "Another version of dtdl is detected at '$(which dtdl)'. Would you like to update it? (requires superuser, i.e. your password) [y/n]: " updt
	fi
	updt=$(echo $updt | tr '[:lower:]' '[:upper:]')
    while [ "$updt" != 'Y' ] && [ "$updt" != 'N' ]; do 
		read -p "Enter 'y' or 'n': " updt
		updt=$(echo $updt | tr '[:lower:]' '[:upper:]')
	done
	if [ $updt = 'Y' ] && [ $(which dtdl | grep '^/home') ]; then
    	cp dist/dtdl $(which dtdl)
		copied=1
	elif [ $updt = 'Y' ]; then
		sudo cp dist/dtdl $(which dtdl)
		if [ $? = 0 ]; then
			copied=1
		fi
	fi
fi
if [ $copied = 0 ]; then
    whchpth='U'
    read -p "Would you like to make the program available to all users? (requires superuser, i.e. your password) [y/n]: " whchpth
	whchpth=$(echo $whchpth | tr '[:lower:]' '[:upper:]')
    while [ "$whchpth" != 'Y' ] && [ "$whchpth" != 'N' ]; do 
		read -p "Enter 'y' or 'n': " whchpth
		whchpth=$(echo $whchpth | tr '[:lower:]' '[:upper:]')
	done
    if [ $whchpth = 'Y' ]; then
        sudo cp dist/dtdl /usr/bin/ 2> /dev/null
		if [ $? = 0 ]; then
			copied=1
		fi
    fi
    if [ $? != 0 ] || [ $whchpth = 'N' ]; then
        mkdir -p ~/.local/bin/
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
		copied=1
    fi
fi

which dtdl > /dev/null 2>&1
if [ $? != 0 ]; then
    echo "Error. Is '~/.local/bin' in your PATH variable?"
    exit 1
elif [ $copied = 0 ]; then
	echo "Error. Program not installed."
	exit 1
else
    echo "Installed to $(which dtdl)"
fi
exit 0
