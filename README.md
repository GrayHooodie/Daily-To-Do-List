# Daily To-Do List

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
Move into the project folder, and run the following command:
**python3 dtdl.py**


## Configuration

A file called *tweaks.conf* is located at *~/.dtdl/config/tweaks.conf*. You can edit the contents of this file with your text editor of choice. The syntax of these tweak values is:
**twkname=value**

where *twkname* is the name of the tweak, and *value* is a number.

If you make a mistake and need to reference the default *tweaks.conf*, it's located at *Daily-To-Do-List/defaults/tweaks.conf*. Or, if you want to start over, simply delete the *tweaks.conf* file located at *~/.dtdl/config/tweaks.conf* and run **./install.sh** in the project folder.