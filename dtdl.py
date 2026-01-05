# Simple todo-list program made by Matt L on 2025/12/11 while not wanting to go to sleep
from os import system

import modules.disp as disp
import modules.fman as fman
import modules.gnrl as gnrl
import modules.progfuncs as pf

def main() -> int:
	gnrl.file_integrity()
	todo = fman.autoload()
	disp.menu(todo, True)
	while True:
		item = input(" > ")
		if item.isdigit():
			item = int(item) - 1
			if item in range(len(todo)):
				pf.cross(todo, item)		
				disp.menu(todo, False)
			else:
				gnrl.slowprint("Please enter a valid line number to cross-off.")
		else:
			match item:
				case '':
					disp.menu(todo, False)
				case 's':
					todo = pf.sort_items(todo)
					disp.menu(todo, False)
				case 'a' | 'A':
					if len(todo) > 1:
						todo = pf.arrange_items(todo)
						disp.return_to_menu(todo)
					else:
						gnrl.slowprint("Must have at least 2 list items to arrange.")
				case 'e' | 'E':
					if len(todo) > 0:
						todo = pf.edit_items(todo)
						disp.return_to_menu(todo)
					else:
						gnrl.slowprint("Must have at least 1 list item to edit.")
				case 'p' | 'P':
					todo = pf.postpone_items(todo)
					disp.return_to_menu(todo)	
				case 'r' | 'R':
					if len(todo) > 0:
						todo = pf.rm_items(todo)
						disp.return_to_menu(todo)
					else:
						gnrl.slowprint("Must have at least 1 list item to remove.")
				case 'c' | 'C':
					todo = pf.clear(todo)
					disp.return_to_menu(todo)
				case 'S':
					if len(todo) > 0:
						pf.save(todo)
						disp.return_to_menu(todo)
					else:
						gnrl.slowprint("Must have a list to save.")
				case 'l' | 'L':
					todo = pf.load(todo)
					disp.return_to_menu(todo)
				case 'h' | 'H':
					gnrl.slowprint('', "'s'  Sort Items", "'a'  Arrange Items", "'e'  Edit Items", "'p'  Postpone Items", "'r'  Remove Items", '', "'C'  Clear List", "'S'  Save List To File", "'L'  Load List From File", '', "'h'  Show This Help Text", "'q'  Quit", '')
				case 'q' | 'Q':
					if len(todo):
						fman.autosave(todo)
					system("clear")
					return 0
				case _:
					if len(item) > 1:
						todo.append(item)
						disp.menu(todo, False)
					else:
						gnrl.slowprint(f"Unknown command '{item}'.") 

if __name__ == "__main__":
	main()
