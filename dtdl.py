# Simple todo-list program made by Matt L on 2025/12/11 while not wanting to go to sleep
from subprocess import call
import sys

RELEASE_NUM = "v1.1.0"

if len(sys.argv) > 1:
	if len(sys.argv) > 2:
		print("\ndtdl can only take one flag for input ('-v', '--version', 'h', '--help').\n")
	elif sys.argv[1] in ["-v", "--version", "-h", "--help"]:
		if 'v' in sys.argv[1]:
			print(f"\ndtdl --- {RELEASE_NUM}\n")
		elif 'h' in sys.argv[1]:
			print("\n'-v', '--version'    ---    Show the current installed version of the program")
			print("'-h', '--help'       ---    Show this help screen\n")
		sys.exit(0)
	else:
		print(f"\nUnknown flag '{sys.argv[1]}'. You may use one of the following flags: '-v', '--version', '-h', '--help'\n")
	sys.exit(1)

from modules.setup import file_integrity
import modules.disp as disp
import modules.fman as fman
import modules.glob as glob
import modules.gnrl as gnrl
import modules.progfuncs as pf
import modules.twks as twks

@gnrl.ctrl_c_handler
def main() -> int:
	while True:
		glob.unchanged = []
		file_integrity()
		disp.menu(glob.show_title, glob.bypass)
		if glob.bypass:
			glob.bypass = False
		if glob.show_title:
			glob.show_title = False
		item = input(" > ")
		if item.isdigit():
			item = int(item) - 1
			if item in range(len(glob.todo)):
				pf.cross(item)		
			else:
				gnrl.slowprint("Please enter a valid line number to cross-off.")
		elif len(item) > 1 and item[0].lower() == 'p' and item[1:].isdigit():
			if int(item[1:]) in range(twks.pages + 1):
				twks.page = int(item[1:])
			elif twks.pages == 1:
				gnrl.slowprint("You only have one page of list items.")
				glob.bypass = True
			else:
				gnrl.slowprint("Please enter a valid page number.")
				glob.bypass = True
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
						glob.bypass = True
				case 'e' | 'E':
					if len(glob.todo):
						pf.edit_items()
					else:
						gnrl.slowprint("Must have at least 1 list item to edit.")
						glob.bypass = True
				case 'p' | 'P':
					open_file = fman.read_open_file()
					if not len(open_file):
						gnrl.slowprint("Must have a saved 'daily' list open to postpone items.")
						glob.bypass = True
					elif open_file['type'] == "%c":
						gnrl.slowprint("Must be a 'daily' to-do list to postpone items. A 'daily' to-do list is one that is named with the default of the current day's date.")
						glob.bypass = True
					else:
						pf.postpone_items()
				case 'r' | 'R':
					if len(glob.todo):
						pf.rm_items()
					else:
						gnrl.slowprint("Must have at least 1 list item to remove.")
						glob.bypass = True
				case 'c' | 'C':
					pf.clear()
				case 'S':
					if len(glob.todo):
						pf.save()
					else:
						gnrl.slowprint("Must have at least 1 list item to save.")
						glob.bypass = True
				case 'l' | 'L':
					if len(fman.get_file_names()):
						pf.load()
					else:
						gnrl.slowprint("Must have at least 1 saved list to load.")
						glob.bypass = True
				case 'h' | 'H':
					gnrl.slowprint(
					'',
					"'s'  Sort Items",
					"'a'  Arrange Items",
					"'e'  Edit Items",
					"'r'  Remove Items",
					"'p'  Postpone Items / Switch Page (when followed by a digit)",
					'',
					"'C'  Clear List / Close File",
					"'S'  Save List To File",
					"'L'  Load List From File",
					'',
					"'h'  Show This Help Text",
					"'q'  Quit",
					''
					)
					glob.bypass = True
				case 'q' | 'Q':
					open_file = fman.read_open_file()
					if len(open_file) or len(glob.todo):
						pf.autosave(using_clear=False)
					call(glob.clear)
					return 0
				case _:
					if len(item) > 1:
						glob.todo.append(item)
					else:
						gnrl.slowprint(f"Unknown command '{item}'.") 
						glob.bypass = True

if __name__ == "__main__":
	fman.autoload()
	main()
