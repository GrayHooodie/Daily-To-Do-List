# Daily To-Do List

## Prerequisites
In order to run from source, Python version 3.10.0 or newer must be installed. Running from an installed version does not require Python.


## Installation

### Main or Staging Branch
Clone the repository and run the following command while in the project folder:

> ./install.sh


### Other Branches
Clone the repository and run the following commands while in the project folder:

> ./compile.sh

> ./install.sh


## Using Daily-To-Do-List

### Running The Program

#### After Install
Simply type the following command into your terminal:

> dtdl


#### From Source
Python must be version 3.10.0 or newer. Move into the project folder, and run the following command:

> python3 dtdl.py


### Program Flags
You can add the following flags after *'dtdl '* to get the corresponding information:

'-h' or '--help'        Show the available flags
'-v' or '--version'     Show the program's installed version


### Running The Program

#### Basic Functionality
Type in an item you want to add to your to-do list, then hit enter. If you then finish that task, you can type in the line number it's on, hit enter, then it will be crossed off.


#### List Manipulation
The operations you can use on your list are:
- Sort Items
- Arrange items
- Edit Items
- Remove Items, and
- Postpone Items (only in a daily to-do list)

The commands to use these operations are shown inside the single quotes ('') below, and are always followed by the enter key.


##### Sort Items
's' (lowercase) will pull the crossed-off items in your to-do list to the bottom so you can focus on what needs to get done.

There is no "sort items" menu, it simply sorts your list in the main menu.


##### Arrange Items
'a' (case-insensitive) will bring you to the "arranging items" menu, where you can arrange the items in your to-do list.


###### Main Usage
First, enter the line number of the item you would like to move. Then, enter the line number that you would like it to be moved to. Repeat as necessary. Once you're done arranging items, press enter to confirm changes.


###### Cancelling Changes
'c' (case-insensitive), when entered after selecting a line to move, will cancel the moving of that line and return you to the "arranging items" menu. When instead entered in the "arranging items" menu, you will be brought back to the main menu erasing all changes made.


##### Edit Items
'e' (case-insensitive) will bring you to the "editing items" menu, where you can edit the text of your list items individually.


###### Main Usage
First, enter the line number of the item you would like to change the text of. Then, enter the new text of the line. Repeat as necessary. Once you're done editing items, press enter to confirm changes.


###### Cancelling Changes
'c' (case-insensitive), when entered after selecting a line to edit, will cancel the editing of that line and return you to the "editing items" menu. When instead entered in the "editing items" menu, you will be brought back to the main menu erasing all changes made.


##### Remove Items
'r' (case-insensitive) will bring you to the "removing items" menu, where items can be deleted rather than crossed off.


###### Main Usage
First, enter the line number of the item you would like to remove. Repeat as necessary. Once you're done removing items, press enter to confirm changes.


###### Cancelling Changes
'c' (case-insensitive) will revert any line removals, and bring you back to the main menu.


##### Postpone Items (only in a daily to-do list)
'p' (case-insnsitive) will bring you to the "postponing items" menu, where items can be deferred to the next day.


###### Main Usage
First, enter the line number of the item you would like to postpone. Repeat as necessary. Once you're done postponing items, press enter to confirm changes.


###### Cancelling Changes
'c' (case-instensitive) will revert any postponements of items, and bring you back to the main menu.


#### List File Manipulation
The file-related operations you can use on your list are:
- Clear List / Close File
- Save List To File
- Load List From File (and the subsequent file operations)

The commands to use these operations are shown inside the single quotes ('') below, and are always followed by the enter key.


##### Clear List / Close File
'C' (case-insensitive), depending on if you have a list open or not, will ask you if you want to close your current to-do list file, or clear your current to-do list, respectively. An open list file will be saved automatically. Enter 'y' or 'N' (case-insensitive, prefers 'N') to confirm or cancel the clearing/closing of your to-do list (saving the file).


##### Save List To File
'S' (capitalized) will bring you to the "saving file" menu, where you can save your current to-do list to a file.


###### Main Usage
If you have a file open, you can press enter to automatically save to that same file. Otherwise, if you don't already have today's daily to-do list file, you can press enter to automatically set the name of your new file to today's date and make it a daily to-do list.

If you want to save your file with a custom name, enter the name you wish to name your file with. A custom file name cannot be a date in the format of YYYY-MM-DD.

If you would rather overwrite a file, enter the same name or the line number of the file you wish to overwrite. Enter 'y' or 'N' (case-insensitive, prefers 'N') to confirm or cancel the overwrite, respectively.


###### Cancelling File Save
'c' (case-insensitive) will cancel the saving of your list, and bring you back to the main menu.


##### Load List From File
'L' (case-insensitive) will bring you to the "loading file" menu, where you can load or modify your saved to-do list files.


###### Main Usage
Enter the line number of the file you would like to open.

If the file you currently have open hasn't been saved, it will prompt you asking if you would like to save. Enter 'Y' or 'n' (case-insensitive, prefers 'Y') to confirm or deny the saving of your current open file, respectively.


###### File Modifications
'r' (case-insensitive) will ask you to enter the line number of the file you wish to rename. Then, enter the new name of the file. Daily to-do lists cannot be renamed, nor can other to-do lists be renamed to act as a daily to-do list in the format of YYYY-MM-DD.

'd' (case-insensitive) will ask you to enter the line number of the file you wish to delete. Then, enter 'y' or 'N' (case-insensitive, prefers 'N') to confirm or deny the deletion of the entered file, respectively. If you are trying to delete your current open file, the program will let you know as it prompts for confirmation that your to-do list will be cleared.

'a' (case-insensitive) will ask you to enter the line number of the file you wish to archive. Then, enter 'y' or 'N' (case-insensitive, prefers 'N') to confirm or deny the archival of the entered file, respectively. If you are trying to archive your current open file, the program will let you know as it prompts for confirmation that your to-do list will be cleared.


###### Cancelling File Load
'c' (case-insensitive) will cancel the loading of a list file, and bring you back to the main menu. None of the file modifications will be reverted.


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

