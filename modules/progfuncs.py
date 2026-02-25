from os import listdir, path
from time import sleep

# Local modules imports
import modules.disp as disp
import modules.fman as fman
import modules.glob as glob
import modules.gnrl as gnrl
import modules.twks as twks

# Pushes crossed items to bottom
def sort_items() -> None:
	uncrossed = []
	crossed = []
	for item in glob.todo:
		if ord(item[1]) == 822:
			crossed.append(item)
		else:
			uncrossed.append(item)
	glob.todo = uncrossed + crossed

# Determines if item is crossed, and reverses that
def cross(line: int) -> None:
	if ord(glob.todo[line][1]) == 822:
		glob.todo[line] = gnrl.unstrike(glob.todo[line])
	else:
		glob.todo[line] = gnrl.strike(glob.todo[line])
	return None

# User-interactive function
def arrange_items() -> None:
	glob.unchanged = glob.todo.copy()
	first_text = {'context': "Enter the line number you would like to move. Empty return to finish arranging items. 'c' to cancel.", 'line_num': glob.INV_LINE}
	while True:
		disp.arrange_items_menu()
		line = gnrl.enter_digit(base=1, text=first_text, enter_to_confirm=True)
		if line is None:
			raise ValueError
		if line == -1:
			disp.confirm_edits_text(glob.todo == glob.unchanged, "arranged")
			sleep(glob.SLPTM)
			return None
		elif line == -2:
			gnrl.slowprint('', glob.NO_CHANGE, '')
			glob.todo = glob.unchanged
			sleep(glob.SLPTM)
			return None	
		elif line == -3:
			continue
		second_text = {'context': f"Enter the new position of line {line + 1}. 'c' to cancel line {line + 1} arrangement.", 'line_num': glob.INV_LINE, 'cancel': f"Cancelled arrangement of line {line + 1}."}
		while True:
			dest = gnrl.enter_digit(base=1, text=second_text, enter_to_confirm=False)
			if dest is None:
				raise ValueError
			if dest == -2:
				sleep(glob.SLPTM)
				break
			elif dest == -3:
				disp.arrange_items_menu()
				continue
			else:
				item = glob.todo[line]
				glob.todo.remove(item)
				glob.todo.insert(dest, item)
				break

# User-interactive function
def edit_items() -> None:
	glob.unchanged = glob.todo.copy()
	first_text = {'context': "Enter the line number you would like to edit. Empty return to finish editing items. 'c' to cancel.", 'line_num': glob.INV_LINE}
	while True:
		disp.edit_items_menu()
		line = gnrl.enter_digit(base=1, text=first_text, enter_to_confirm=True)
		if line is None:
			raise ValueError
		if line == -1:
			disp.confirm_edits_text(glob.todo == glob.unchanged, 'edited')
			sleep(glob.SLPTM)
			return None
		elif line == -2:
			gnrl.slowprint('', glob.NO_CHANGE, '')
			glob.todo = glob.unchanged
			sleep(glob.SLPTM)
			return None
		elif line == -3:
			continue
		second_text = {'context': f"Enter the new text for line {line + 1}. 'c' to cancel edits on line {line + 1}.", 'number': "Item can't be a number.", 'cancel': f"Cancelled edits on line {line + 1}.", 'length': "Item must be two or more characters."}
		edited = edit_item_text(second_text)
		if edited == 'c':
			sleep(glob.SLPTM)
			continue
		glob.todo.pop(line)
		glob.todo.insert(line, edited)

# Break up parent function ^
def edit_item_text(text: dict) -> str:
	minlength = 2
	gnrl.slowprint('', text['context'], '')
	while True:
		edited = input(" > ")
		if edited.isdigit():
			gnrl.slowprint(text['number'])
		elif len(edited) >= minlength:
			return edited
		elif edited.lower() == 'c':
			gnrl.slowprint('', text['cancel'], '')
			return edited
		else:
			gnrl.slowprint(text['length'])

# User-interactive function
def postpone_items() -> None:
	glob.unchanged = glob.todo.copy()
	to_postpone = []
	text = {'context': "Enter line number(s) to postpone. Empty return to finish postponing items. 'c' to cancel.", 'line_num': glob.INV_LINE, 'crossed': "Item can't be crossed-off."}
	while True:
		disp.postpone_items_menu()
		line = gnrl.enter_digit(base=1, text=text, enter_to_confirm=True)
		if line is None:
			raise ValueError
		if line == -1:
			break
		elif line == -2:
			gnrl.slowprint('', glob.NO_CHANGE, '')
			glob.todo = glob.unchanged	
			sleep(glob.SLPTM)	
			return None
		elif line == -3:
			continue
		to_postpone.append(glob.todo[line])	
		glob.todo.pop(line)
	if len(to_postpone):	
		add_to_postpone(to_postpone)	
	disp.confirm_edits_text(glob.todo == glob.unchanged, "postponed")
	sleep(glob.SLPTM)	
	return None

# Break up parent function ^
def add_to_postpone(to_postpone: list[str]) -> None:
	with open(path.join(glob.PROGFILES, "postpone"), 'a') as f:
		for item in to_postpone:
			f.write(f"{item}\n")	
	return None

# User-interactive function
def rm_items() -> None:
	glob.unchanged = glob.todo.copy()
	text = {'context': "Enter line number(s) to remove. Empty return to finish removing items. 'c' to cancel.", 'line_num': glob.INV_LINE}
	while True:
		disp.rm_items_menu()
		line = gnrl.enter_digit(base=1, text=text, enter_to_confirm=True)
		if line is None:
			raise ValueError
		if line == -1:
			disp.confirm_edits_text(glob.todo == glob.unchanged, "removed")	
			sleep(glob.SLPTM)	
			return None
		elif line == -2:
			gnrl.slowprint('', glob.NO_CHANGE, '')
			glob.todo = glob.unchanged
			sleep(glob.SLPTM)
			return None
		elif line == -3:
			continue
		glob.todo.pop(line)

# Clears/closes list after a prompt to the user
def clear() -> None:
	open_file = fman.read_open_file()
	if len(open_file):
		gnrl.slowprint('', f"Are you sure you want to close file '{open_file['name']}'? Progress will be saved. (y/N)", '')
	else:
		gnrl.slowprint('', "Are you sure you want to clear your to-do list? (y/N)", '')
	while True:
		check = input(" > ")
		match check:
			case 'y' | 'Y':
				if len(open_file):
					saved = autosave(using_clear=True)
				else:
					saved = False
				fman.clear_open_file()
				glob.todo = []
				if len(open_file):
					if saved:
						gnrl.slowprint('', f"File successfully closed. Progress successfully saved to '{path.join(glob.LISTFILES, open_file['name'])}'.", '')
					else:
						gnrl.slowprint('', "File successfully closed.", '')
				else:
					gnrl.slowprint('', "To-do list successfully cleared.", '')
				sleep(glob.SLPTM)	
				return None
			case 'n' | 'N' | '':
				gnrl.slowprint('', glob.NO_CHANGE, '')
				sleep(glob.SLPTM)
				return None 
			case _:
				gnrl.slowprint(glob.Y_OR_N)

# Used when closing program or closing file
def autosave(using_clear: bool) -> bool:
	open_file = fman.read_open_file()
	if len(open_file):
		last_saved = fman.open_list(open_file['name'])
		if len(last_saved):
			last_saved.pop()
			if glob.todo == last_saved:
				return False
	if (len(open_file)) or (f"{glob.date}.todo" not in listdir(glob.LISTFILES)):
		if open_file['name'] == f"{glob.date}.todo":
			files = fman.get_file_names()
			fman.move_old_dailys(files)
		with open(path.join(glob.LISTFILES, open_file['name']), 'w') as f:
			for item in glob.todo:
				f.write(f"{item}\n")
			f.write(f"{open_file['type']}\n")
		if not using_clear:	
			gnrl.slowprint('', f"List successfully saved to '{path.join(glob.LISTFILES, open_file['name'])}'.", '')
			sleep(glob.SLPTM)
	else:
		prompt_save()
	return True

# User-interactive function
def save() -> None:
	disp.save_menu()
	files = fman.get_file_names()
	open_file = fman.read_open_file()
	while True:
		file: str = input(" > ")
		if file.isdigit():
			file: int = int(file) - 1
			if file in range(len(files)):
				if overwrite_save(files[file]):
					file: str = files[file].split(glob.EXT)[0]
					break
			else:
				gnrl.slowprint("Please enter a valid file number, or name your file.")
		elif file == '':
			if len(open_file):
				file: str = open_file['name'].split(glob.EXT)[0]
				if open_file['name'].split(glob.EXT)[0] == glob.date:
					fman.move_old_dailys(files)
				break
			elif f"{glob.date}.todo" not in files:
				file: str = glob.date
				fman.move_old_dailys(files)
				break
			else:
				gnrl.slowprint("Please name your file.")
		elif file == 'c':
			gnrl.slowprint('', "Cancelled file save.", '')
			sleep(glob.SLPTM)
			return None
		elif gnrl.is_daily(file):
			gnrl.slowprint("Name can't be a date in the format of 'YYYY-MM-DD'.")
		elif f"{file}.todo" in files:
			if overwrite_save(f"{file}.todo"):
				break
		elif glob.ext in file:
			gnrl.slowprint("Name can't contain '.todo'.")
		else:
			break
	identifier: str = fman.select_identifier(file)
	with open(path.join(glob.PROGFILES, "lastopen"), 'w') as f:
		f.write(f"{file}.todo\n{identifier}\n")
	with open(path.join(glob.LISTFILES, f"{file}.todo"), 'w') as f:
		for item in glob.todo:
			f.write(f"{item}\n")
		f.write(f"{identifier}\n")
	gnrl.slowprint('', f"List successfully saved to '{path.join(glob.LISTFILES, file)}.todo'.", '')
	sleep(glob.SLPTM)
	return None

# If no file is open (e.g. can't autosave)
def prompt_save() -> None:
	gnrl.slowprint('', "Would you like to save your current to-do list? (Y/n)", '')
	while True:
		will_save = input(" > ")
		match will_save:
			case 'n' | 'N':
				return None
			case 'y' | 'Y' | '':
				save()
				return None
			case _:
				gnrl.slowprint(glob.Y_OR_N)

# Break down parent function (save)
def overwrite_save(filename: str) -> bool:
	gnrl.slowprint('', f"'{filename}' already exists. Would you like to overwrite it? (y/N)", '')
	while True:
		will_overwrite = input(" > ")
		match will_overwrite:
			case 'n' | 'N' | '':
				disp.save_menu()
				return False
			case 'y' | 'Y':
				return True
			case _:
				gnrl.slowprint(glob.Y_OR_N)

# User-interactive function
def load() -> None:
	glob.unchanged = glob.todo.copy()
	invalid_line = False	
	while True:
		if not len(fman.get_file_names()):
			gnrl.slowprint('', "No files to show.", '')
			sleep(glob.SLPTM)
			return None
		if not invalid_line:
			disp.load_menu()
		else:
			invalid_line = False
		files = fman.get_file_names()
		open_file = fman.read_open_file()
		select = input(" > ").lower()
		if select.isdigit():
			select = int(select) - 1
			if select in range(len(files)):
				if len(open_file):
					last_saved = fman.open_list(open_file['name'])
					if len(last_saved):
						last_saved.pop()
					if glob.todo != last_saved:
						prompt_save()
				elif len(glob.todo):
					prompt_save()
				glob.todo = fman.open_list(files[select])
				if not len(glob.todo):
					if fman.empty_file_delete(files[select]):
						gnrl.slowprint('', f"File '{files[select]}' successfully deleted.", '')
						sleep(glob.SLPTM)
						continue
					else:
						glob.todo = fman.open_list(files[select])
				with open(path.join(glob.PROGFILES, "lastopen"), 'w') as f:
					f.write(f"{files[select]}\n{glob.todo[-1]}\n")
				glob.todo.pop()
				break
			else:
				gnrl.slowprint(glob.INV_FUNC)
				invalid_line = True
		else:
			match select:
				case 'c':
					gnrl.slowprint('', "No file loaded.", '')
					sleep(glob.SLPTM)
					return None
				case 'r':	
					fman.rename_load_file(files)
				case 'a':
					fman.archive_load_file(files)
				case 'd':		
					fman.delete_load_file(files)
				case _:
					gnrl.slowprint(glob.INV_FUNC)
					invalid_line = True
	gnrl.slowprint('', f"File '{files[select]}' successfully loaded.", '')
	twks.page = 1
	sleep(glob.SLPTM)
	return None
	