# Daily To-Do List

## Installation

### Main Branch
Simply run the following command while in the project folder:
**./installer.sh**

### Staging/Dev/Other Branch
Python and PyInstaller must be installed. Run the following commands while in the project folder:
**./compile.sh**
**./installer.sh**


## Configuration

A file called *tweaks.conf* is located at *~/.dtdl/config/tweaks.conf*. You can edit the contents of this file with your text editor of choice. The syntax of these tweak values is:
**twkname=value**

where *twkname* is the name of the tweak, and *value* is a number.

If you make a mistake and need to reference the default *tweaks.conf*, it's located at *Daily-To-Do-List/defaults/tweaks.conf*. Or, if you want to start over, simply delete the *tweaks.conf* file located at *~/.dtdl/config/tweaks.conf* and it will be copied from the *defaults* folder the next time you open the application.