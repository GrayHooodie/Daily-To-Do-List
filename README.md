# Daily To-Do List

## Prerequisites
Python must be installed to run from source.


## Installation

### Main or Staging Branch
Clone the repository and run the following command while in the project folder:

> ./install.sh


### Other Branches
Clone the repository and run the following commands while in the project folder:

> ./compile.sh
> ./install.sh


## Running Daily-To-Do-List

### After Install
Simply type the following command into your terminal:

> dtdl


### From Source
Python must be version ^.^.^ or newer. Move into the project folder, and run the following command:

> python3 dtdl.py


## Configuration

### Overview
A file called *tweaks.conf* is located at *~/.dtdl/config/tweaks.conf*. You can edit the contents of this file with your text editor of choice. The syntax of these tweak values is:

> twkname=value

where *twkname* is the name of the tweak, and *value* is a number.

If you need to reference the defaults, read **Available Tweaks** below. Or, if you want to start over, simply delete the *tweaks.conf* file located at *~/.dtdl/config/tweaks.conf* and it will be regenerated the next time you open the program.

### Available Tweaks
So far, only two tweaks are available: *pagelength* and *textspeed*.

#### pagelength
This is how many list items will show up on a single page. This can make a huge difference if you're using this on a phone terminal emulator, or a small laptop screen. Default is 50.

How it appears in the *tweaks.conf* file:

> pagelength=50


#### textspeed
This is how many seconds between 2 lines of text (global to the whole program). Anything larger than 0.05 is not recommended for serious use. 0.0, or just 0, will make text appear instantly. Default is 0.02.

How it appears in the *tweaks.conf* file:

> textspeed=0.02