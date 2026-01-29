# Simple todo-list program made by Matt L on 2025/12/11 while not wanting to go to sleep
from os import system

import modules.disp as disp
import modules.fman as fman
import modules.glob as glob
import modules.gnrl as gnrl
import modules.progfuncs as pf

maxlength = glob.get_tweak_int("maxvalue", 50)
textspeed = glob.get_tweak_float("textspeed", 0.02)

def main() -> int:
	fman.file_integrity()
	fman.autoload()
	page = 1
	show_title: bool = True
	bypass: bool = False
	while True:
		pages = (len(glob.todo) / maxlength) + (len(glob.todo) % maxlength > 0)	
		disp.menu(show_title, bypass, page, pages)
		if bypass:
			bypass = False
		if show_title:
			show_title = False
		item = input(" > ")
		if item.isdigit():
			item = int(item) - 1
			if item in range(len(glob.todo)):
				pf.cross(item)		
			else:
				gnrl.slowprint("Please enter a valid line number to cross-off.")
		elif len(item) > 1 and item[0].lower() == 'p' and item[1:].isdigit():
			if int(item[1:]) in range(pages):
				page = int(item[1:])
			else:
				gnrl.slowprint("Please enter a valid page number.")
				bypass = True
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
						bypass = True
				case 'e' | 'E':
					if len(glob.todo):
						pf.edit_items()
					else:
						gnrl.slowprint("Must have at least 1 list item to edit.")
						bypass = True
				case 'p' | 'P':
					open_file = fman.read_open_file()
					if not len(open_file):
						gnrl.slowprint("Must have a saved 'daily' list open to postpone items.")
						bypass = True
					elif open_file["lstype"] == "%c":
						gnrl.slowprint("Must be a 'daily' to-do list to postpone items. A 'daily' to-do list is one that is named with the default of the current day's date.")
						bypass = True
					else:
						pf.postpone_items()
				case 'r' | 'R':
					if len(glob.todo):
						pf.rm_items()
					else:
						gnrl.slowprint("Must have at least 1 list item to remove.")
						bypass = True
				case 'c' | 'C':
					pf.clear()
				case 'S':
					if len(glob.todo):
						pf.save()
					else:
						gnrl.slowprint("Must have at least 1 list item to save.")
						bypass = True
				case 'l' | 'L':
					if len(fman.get_file_names()):
						pf.load()
					else:
						gnrl.slowprint("Must have at least 1 saved list to load.")
						bypass = True
				case 'h' | 'H':
					gnrl.slowprint('', "'s'  Sort Items", "'a'  Arrange Items", "'e'  Edit Items", "'p'  Postpone Items", "'r'  Remove Items", '', "'C'  Clear List / Close File", "'S'  Save List To File", "'L'  Load List From File", '', "'h'  Show This Help Text", "'q'  Quit", '')
					bypass = True
				case 'q' | 'Q':
					open_file = fman.read_open_file()
					if len(open_file) or len(glob.todo):
						pf.autosave(False)
					system(glob.clear)
					return 0
				case _:
					if len(item) > 1:
						glob.todo.append(item)
					else:
						gnrl.slowprint(f"Unknown command '{item}'.") 
						bypass = True

if __name__ == "__main__":
	main()
