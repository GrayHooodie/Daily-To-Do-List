# Simple todo-list program made by Matt L on 2025/12/11 while not wanting to go to sleep
from os import system

import modules.disp as disp
import modules.fman as fman
import modules.glob as glob
import modules.gnrl as gnrl
import modules.progfuncs as pf

def main() -> int:
	fman.file_integrity()
	fman.autoload()
	show_title: bool = True
	helping: bool = False
	while True:
		if not helping:
			disp.menu(show_title)
		helping = False
		item = input(" > ")
		if item.isdigit():
			item = int(item) - 1
			if item in range(len(glob.todo)):
				pf.cross(item)		
			else:
				gnrl.slowprint("Please enter a valid line number to cross-off.")
		else:
			match item:
				case '':
					pass
				case 's':
					pf.sort_items()
				case 'a' | 'A':
					if len(glob.todo) > 1:
						pf.arrange_items()
					else:
						gnrl.slowprint("Must have at least 2 list items to arrange.")
				case 'e' | 'E':
					if len(glob.todo) > 0:
						pf.edit_items()
					else:
						gnrl.slowprint("Must have at least 1 list item to edit.")
				case 'p' | 'P':
					open_file = fman.read_open_file()
					if not len(open_file):
						gnrl.slowprint("Must have a saved file open to postpone items.")
					elif open_file["lstype"] == "%c":
						gnrl.slowprint("File must be a 'daily' to-do list to postpone items. A 'daily' to-do list is one that is named with the default of the current day's date.")
					else:
						pf.postpone_items()
				case 'r' | 'R':
					if len(glob.todo) > 0:
						pf.rm_items()
					else:
						gnrl.slowprint("Must have at least 1 list item to remove.")
				case 'c' | 'C':
					pf.clear()
				case 'S':
					if len(glob.todo) > 0:
						pf.save()
					else:
						gnrl.slowprint("Must have a list to save.")
				case 'l' | 'L':
					pf.load()
				case 'h' | 'H':
					gnrl.slowprint('', "'s'  Sort Items", "'a'  Arrange Items", "'e'  Edit Items", "'p'  Postpone Items", "'r'  Remove Items", '', "'C'  Clear List", "'S'  Save List To File", "'L'  Load List From File", '', "'h'  Show This Help Text", "'q'  Quit", '')
					helping = True
				case 'q' | 'Q':
					open_file = fman.read_open_file()
					if len(open_file) or len(glob.todo):
						pf.autosave()
					system(glob.clear)
					return 0
				case _:
					if len(item) > 1:
						glob.todo.append(item)
					else:
						gnrl.slowprint(f"Unknown command '{item}'.") 
		if show_title:
			show_title = False	

if __name__ == "__main__":
	main()
