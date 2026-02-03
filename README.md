# Daily To-Do List

## Prerequisites
Python must be installed


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
So far, you can only change the pagelength. The pagelength is how many to-do list items will show on one page as an integer. The default is 50.

If you open *~/.dtdl/config/tweaks.conf* with a text editor, you will find:
**pagelength=50**

Simply change the 50 to whatever you feel looks best on your monitor in the program.