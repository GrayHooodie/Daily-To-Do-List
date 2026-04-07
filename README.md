# Daily To-Do List

## Prerequisites
In order to run from source, Python version 3.10.0 or newer must be installed. Running from an installed version does not require Python.


## Installation

### Main or Staging Branch
Clone the repository and run the following command while in the project folder:

> ./install


### Other Branches
Clone the repository and run the following commands while in the project folder:

> ./compile

> ./install


## Uninstallation
While in the project folder, run the following command:

> ./uninstall

This will remove any dtdl binaries, as well as the configuation files (given that all binaries are delete), from your system. To-do list files will remain at their location at '/home/$USER/Documents/To-Do Lists/'.


## Configuration

### Default Items
A file called *daily-default* is located at *~/.dtdl/config/daily-default*. You can add items to the text file, separated by a return key, and they will be added to every new daily to-do list automatically. Here is the correct formatting:

> Do dishes

> Call Mom

> Take out trash

Save the file, then every sequencial daily to-do list will have each item added automatically.


### Tweaks
A file called *tweaks.conf* is located at *~/.dtdl/config/tweaks.conf*. You can edit the contents of this file with your text editor of choice. The syntax of these tweak values is:

> twkname=value

where *twkname* is the name of the tweak, and *value* is a number. Any changes made will be applied the next time you open the program.

If you need to reference the defaults, read **Available Tweaks** below. Or, if you want to start over, simply delete the *tweaks.conf* file located at *~/.dtdl/config/tweaks.conf* and it will be regenerated the next time you open the program.


#### Available Tweaks
So far, only two tweaks are available: *pagelength* and *textspeed*.


##### pagelength
This is how many list items will show up on a single page. This can make a huge difference if you're using this on a phone terminal emulator, or a small or low resolution laptop screen. Default is 50.

How it appears in the *tweaks.conf* file:

> pagelength=50


##### textspeed
This is how many seconds between 2 lines of text (global to the whole program). Anything larger than 0.05 is not recommended for serious use. 0.0, or just 0, will make text appear instantly. Default is 0.02.

How it appears in the *tweaks.conf* file:

> textspeed=0.02
