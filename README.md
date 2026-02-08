# Daily To-Do List

## Prerequisites
Python must be installed. Running the *install.sh* script will do this for you if you use apt, dnf, zypper, or pacman.


## Installation

### Main Branch
Simply clone the repository, and run the following command while in the project folder:
**./install.sh**

### Other Branches
Python and PyInstaller must be installed. Clone the repository and run the following commands while in the project folder:
**./compile.sh**
**./install.sh**


## Running Daily-To-Do-List

### After Install
Simply type the following command into your terminal:
**dtdl**

### From Source
Python must be version ^.^.^ or newer. Move into the project folder, and run the following command:
**python3 dtdl.py**


## Configuration

### Overview
A file called *tweaks.conf* is located at *~/.dtdl/config/tweaks.conf*. You can edit the contents of this file with your text editor of choice. The syntax of these tweak values is:
**twkname=value**

where *twkname* is the name of the tweak, and *value* is a number.

If you make a mistake and need to reference the default *tweaks.conf*, it's located at *Daily-To-Do-List/defaults/tweaks.conf*. Or, if you want to start over, simply delete the *tweaks.conf* file located at *~/.dtdl/config/tweaks.conf* and run **./install.sh** in the project folder.

### Available Tweaks
So far, only two tweaks are available, *pagelength* and *textspeed*.

#### pagelength
This is how many list items will show up on a single page. This can make a huge difference if you're using this on a phone terminal emulator, or a small laptop screen. Default is 50.

#### textspeed
This is how many seconds between 2 lines of text (global to the whole program). Anything larger than 0.05 is not recommended for serious use. 0.0, or just 0, will make text appear instantly. Default is 0.02.