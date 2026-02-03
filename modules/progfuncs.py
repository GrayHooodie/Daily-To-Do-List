from os import listdir, path
from time import sleep

import modules.disp as disp
import modules.fman as fman
import modules.glob as glob
import modules.gnrl as gnrl
import modules.twks as twks

def sort_items() -> None:
	uncrossed = []
	crossed = []
	for item in glob.todo:
		if ord(item[1]) == 822:
			crossed.append(item)
		else:
			uncrossed.append(item)
	glob.todo = uncrossed + crossed

def cross(line: int) -> None:
	if ord(glob.todo[line][1]) == 822:
		glob.todo[line] = gnrl.unstrike(glob.todo[line])
	else:
		glob.todo[line] = gnrl.strike(glob.todo[line])
	return None

def arrange_items() -> None:
	unchanged = glob.todo.copy()
	first_text = {"context": "Enter the line number you would like to move. Empty return to finish arranging items. 'c' to cancel.", "line_num": glob.invalid_ln}
	while True:
		disp.arrange_items_menu()
		line = gnrl.enter_digit(1, first_text, True)
		if line == -1:
			disp.confirm_edits_text(glob.todo == unchanged, "arranged")
			sleep(glob.slptm)
			return None
		elif line == -2:
			gnrl.slowprint('', glob.no_chng, '')
			glob.todo = unchanged
			sleep(glob.slptm)
			return None	
		elif line == -3:
			continue
		second_text = {"context": f"Enter the new position of line {line + 1}. 'c' to cancel line {line + 1} arrangement.", "line_num": glob.invalid_ln, "cancel": f"Cancelled arrangement of line {line + 1}."}
		while True:
			dest = gnrl.enter_digit(1, second_text, False)
			if dest == -2:
				sleep(glob.slptm)
				break
			elif dest == -3:
				disp.arrange_items_menu()
				continue
			else:
				item = glob.todo[line]
				glob.todo.remove(item)
				glob.todo.insert(dest, item)
				break

def edit_items() -> None:
	unchanged = glob.todo.copy()
	first_text = {"context": "Enter the line number you would like to edit. Empty return to finish editing items. 'c' to cancel.", "line_num": glob.invalid_ln}
	while True:
		disp.edit_items_menu()
		line = gnrl.enter_digit(1, first_text, True)
		if line == -1:
			disp.confirm_edits_text(glob.todo == unchanged, 'edited')
			sleep(glob.slptm)
			return None
		elif line == -2:
			gnrl.slowprint('', glob.no_chng, '')
			glob.todo = unchanged
			sleep(glob.slptm)
			return None
		elif line == -3:
			continue
		second_text = {"context": f"Enter the new text for line {line + 1}. 'c' to cancel edits on line {line + 1}.", "number": "Item can't be a number.", "cancel": f"Cancelled edits on line {line + 1}.", "length": "Item must be two or more characters."}
		edited = edit_item_text(second_text)
		if edited == 'c':
			sleep(glob.slptm)
			continue
		glob.todo.pop(line)
		glob.todo.insert(line, edited)

def edit_item_text(text: dict) -> str:
	minlength = 2
	gnrl.slowprint('', text["context"], '')
	while True:
		edited = input(" > ")
		if edited.isdigit():
			gnrl.slowprint(text["number"])
		elif len(edited) >= minlength:
			return edited
		elif edited.lower() == 'c':
			gnrl.slowprint('', text["cancel"], '')
			return edited
		else:
			gnrl.slowprint(text["length"])

def postpone_items() -> None:
	unchanged = glob.todo.copy()
	to_postpone = []
	text = {"context": "Enter line number(s) to postpone. Empty return to finish postponing items. 'c' to cancel.", "line_num": glob.invalid_ln, "crossed": "Item can't be crossed-off."}
	while True:
		disp.postpone_items_menu()
		line = gnrl.enter_digit(1, text, True)
		if line == -1:
			break
		elif line == -2:
			gnrl.slowprint('', glob.no_chng, '')
			glob.todo = unchanged	
			sleep(glob.slptm)	
			return None
		elif line == -3:
			continue
		to_postpone.append(glob.todo[line])	
		glob.todo.pop(line)
	if len(to_postpone):	
		add_to_postpone(to_postpone)	
	disp.confirm_edits_text(glob.todo == unchanged, "postponed")
	sleep(glob.slptm)	
	return None

def add_to_postpone(to_postpone: list[str]) -> None:
	with open(path.join(glob.progfiles, "postpone"), 'a') as f:
		for item in to_postpone:
			f.write(f"{item}\n")	
	return None

def rm_items() -> None:
	unchanged = glob.todo.copy()
	text = {"context": "Enter line number(s) to remove. Empty return to finish removing items. 'c' to cancel.", "line_num": glob.invalid_ln}
	while True:
		disp.rm_items_menu()
		line = gnrl.enter_digit(1, text, True)
		if line == -1:
			disp.confirm_edits_text(glob.todo == unchanged, "removed")	
			sleep(glob.slptm)	
			return None
		elif line == -2:
			gnrl.slowprint('', glob.no_chng, '')
			glob.todo = unchanged
			sleep(glob.slptm)
			return None
		elif line == -3:
			continue
		glob.todo.pop(line)

def clear() -> None:
	open_file = fman.read_open_file()
	if len(open_file):
		gnrl.slowprint('', f"Are you sure you want to close file '{open_file["name"]}'? Progress will be saved. (y/N)", '')
	else:
		gnrl.slowprint('', "Are you sure you want to clear your to-do list? (y/N)", '')
	while True:
		check = input(" > ")
		match check:
			case 'y' | 'Y':
				if len(open_file):
					saved = autosave(True)
				fman.clear_open_file()
				glob.todo = []
				if len(open_file):
					if saved:
						gnrl.slowprint('', f"File successfully closed. Progress successfully saved to '{path.join(glob.listfiles, open_file["name"])}'.", '')
					else:
						gnrl.slowprint('', "File successfully closed.", '')
				else:
					gnrl.slowprint('', "To-do list successfully cleared.", '')
				sleep(glob.slptm)	
				return None
			case 'n' | 'N' | '':
				gnrl.slowprint('', glob.no_chng, '')
				sleep(glob.slptm)
				return None 
			case _:
				gnrl.slowprint(glob.y_or_n)

def autosave(using_clear: bool) -> bool:
	open_file = fman.read_open_file()
	if len(open_file):
		last_saved = fman.open_list(open_file["name"])
		if len(last_saved):
			last_saved.pop()
			if glob.todo == last_saved:
				return False
	if (len(open_file)) or (f"{glob.date}.todo" not in listdir(glob.listfiles)):
		files = fman.get_file_names()
		fman.move_old_dailys(files)
		with open(path.join(glob.listfiles, open_file["name"]), 'w') as f:
			for item in glob.todo:
				f.write(f"{item}\n")
			f.write(f"{open_file["lstype"]}\n")
		if not using_clear:	
			gnrl.slowprint('', f"List successfully saved to '{path.join(glob.listfiles, open_file["name"])}'.", '')
			sleep(glob.slptm)
	else:
		prompt_save()
	return True

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
					file: str = files[file].split(glob.ext)[0]
					break
			else:
				gnrl.slowprint("Please enter a valid file number, or name your file.")
		elif file == '':
			if len(open_file):
				file: str = open_file["name"].split(glob.ext)[0]
				break
			elif f"{glob.date}.todo" not in files:
				file: str = glob.date
				fman.move_old_dailys(files)
				break
			else:
				gnrl.slowprint("Please name your file.")
		elif file == 'c':
			gnrl.slowprint('', "Cancelled file save.", '')
			sleep(glob.slptm)
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
	with open(path.join(glob.progfiles, "lastopen"), 'w') as f:
		f.write(f"{file}.todo\n{identifier}\n")
	with open(path.join(glob.listfiles, f"{file}.todo"), 'w') as f:
		for item in glob.todo:
			f.write(f"{item}\n")
		f.write(f"{identifier}\n")
	gnrl.slowprint('', f"List successfully saved to '{path.join(glob.listfiles, file)}.todo'.", '')
	sleep(glob.slptm)
	return None

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
				gnrl.slowprint(glob.y_or_n)

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
				gnrl.slowprint(glob.y_or_n)

def load() -> None:
	unchanged = glob.todo.copy()
	invalid_line = False	
	while True:
		if not len(fman.get_file_names()):
			gnrl.slowprint('', "No files to show.", '')
			sleep(glob.slptm)
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
					last_saved = fman.open_list(open_file["name"])
					if len(last_saved):
						last_saved.pop()
					if glob.todo != last_saved:
						prompt_save()
				elif len(glob.todo):
					prompt_save()
				glob.todo = fman.open_list(files[select])
				if not len(glob.todo):
					if fman.empty_file_delete(files[select]):
						continue
					else:
						glob.todo = fman.open_list(files[select])
				with open(path.join(glob.progfiles, "lastopen"), 'w') as f:
					f.write(f"{files[select]}\n{glob.todo[-1]}\n")
				glob.todo.pop()
				break
			else:
				gnrl.slowprint(glob.invalid_fn)
				invalid_line = True
		else:
			match select:
				case 'c':
					gnrl.slowprint('', "No file loaded.", '')
					sleep(glob.slptm)
					return None
				case 'r':	
					fman.rename_load_file(files)
				case 'a':
					fman.archive_load_file(files)
				case 'd':		
					fman.delete_load_file(files)
				case _:
					gnrl.slowprint(glob.invalid_fn)
					invalid_line = True
	gnrl.slowprint('', f"File '{files[select]}' successfully loaded.", '')
	twks.page = 1
	sleep(glob.slptm)
	return None
	