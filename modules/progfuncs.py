from os import listdir, path
from time import sleep

import modules.disp as disp
import modules.fman as fman
import modules.glob as glob
import modules.gnrl as gnrl

def sort_items(todo: list[str]) -> list[str]:
	uncrossed = []
	crossed = []
	for item in todo:
		if ord(item[1]) == 822:
			crossed.append(item)
		else:
			uncrossed.append(item)
	return uncrossed + crossed

def cross(todo: list[str], line: int) -> list[str]:
	if ord(todo[line][1]) == 822:
		todo[line] = gnrl.unstrike(todo[line])
	else:
		todo[line] = gnrl.strike(todo[line])
	return todo

def arrange_items(todo: list[str]) -> list[str]:
	unchanged = todo.copy()
	disp.arrange_items_menu(todo)
	first_text = ["Enter the line number you would like to move. Empty return to finish arranging items. 'c' to cancel.", glob.invalid_ln]
	while True:
		line = gnrl.enter_digit(1, len(todo), first_text, True)
		if line == -1:
			disp.confirm_edits_text(todo == unchanged, "arranged")
			return todo
		elif line == -2:
			gnrl.slowprint('', glob.no_chng, '')
			return unchanged
		second_text = [f"Enter the new position of line {line + 1}. 'c' to cancel line {line + 1} arrangement.", glob.invalid_ln, f"Cancelled arrangement of line {line + 1}."]
		dest = gnrl.enter_digit(1, len(todo), second_text, False)
		if dest == -2:
			sleep(1)
			disp.arrange_items_menu(todo)
			continue
		item = todo[line]
		todo.remove(item)
		todo.insert(dest, item)
		disp.arrange_items_menu(todo)

def edit_items(todo: list[str]) -> list[str]:
	unchanged = todo.copy()
	disp.edit_items_menu(todo)
	first_text = ["Enter the line number you would like to edit. Empty return to finish editing items. 'c' to cancel.", glob.invalid_ln]
	while True:
		line = gnrl.enter_digit(1, len(todo), first_text, True)
		if line == -1:
			disp.confirm_edits_text(todo == unchanged, 'edited')
			return todo
		elif line == -2:
			gnrl.slowprint('', glob.no_chng, '')
			return unchanged
		second_text = [f"Enter the new text for line {line + 1}. 'c' to cancel edits on line {line + 1}.", "Item can't be a number.", f"Cancelled edits on line {line + 1}", "Item must be two or more characters."]
		edited = edit_item_text(2, second_text)
		if edited == 'c':
			sleep(1)
			disp.edit_items_menu(todo)	
			continue
		todo.remove(todo[line])
		todo.insert(line, edited)
		disp.edit_items_menu(todo)

def edit_item_text(minlength: int, text: list[str]) -> str:
	gnrl.slowprint('', text[0], '')
	while True:
		edited = input(" > ")
		if edited.isdigit():
			gnrl.slowprint(text[1])
			continue
		elif len(edited) >= minlength:
			return edited
		elif edited.lower() == 'c':
			gnrl.slowprint('', text[2], '')
			return edited
		gnrl.slowprint(text[3])

def postpone_items(todo: list[str]) -> list[str]:
	unchanged = todo.copy()
	to_postpone = []
	text = ["Enter line number(s) to postpone. Empty return to finish postponing items. 'c' to cancel.", glob.invalid_ln]
	while True:
		disp.postpone_items_menu(todo)
		line = gnrl.enter_digit(1, len(todo), text, True)
		if line == -1:
			break
		elif line == -2:
			gnrl.slowprint('', glob.no_chng, '')
			return unchanged
		to_postpone.append(todo[line])	
		todo.remove(todo[line])
	add_to_postpone(to_postpone)	
	disp.confirm_edits_text(todo == unchanged, "postponed")	
	return todo

def add_to_postpone(to_postpone: list[str]) -> None:
	with open(path.join(glob.progfiles, "postpone"), 'a') as f:
		for item in to_postpone:
			f.write(f"{item}\n")	
	return None

def rm_items(todo: list[str]) -> list[str]:
	unchanged = todo.copy()
	text = ["Enter line number(s) to remove. Empty return to finish removing items. 'c' to cancel.", glob.invalid_ln]
	while True:
		disp.rm_items_menu(todo)
		line = gnrl.enter_digit(1, len(todo), text, True)
		if line == -1:
			disp.confirm_edits_text(todo == unchanged, "removed")	
			if not len(todo):
				fman.clear_open_file()	
			return todo
		elif line == -2:
			gnrl.slowprint('', glob.no_chng, '')
			return unchanged
		todo.pop(line)

def clear(todo): 
	gnrl.slowprint('', "Are you sure you want to clear your to-do list? (y/N)", '')
	while True:
		check = input(" > ")
		match check:
			case 'y' | 'Y':
				fman.clear_open_file()
				gnrl.slowprint('', "To-do list cleared.", '')
				return []
			case 'n' | 'N' | '':
				gnrl.slowprint('', glob.no_chng, '')
				return todo 
			case _:
				gnrl.slowprint(glob.y_or_n)

def save(todo: list[str]) -> None:
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
			return
		elif gnrl.is_daily(file):
			gnrl.slowprint("Name can't be a glob.date in the format of 'YYYY-MM-DD'.")
		elif f"{file}.todo" in files:
			if overwrite_save(f"{file}.todo"):
				break
		elif glob.ext in file:
			gnrl.slowprint("Name can't contain '.todo'.")
		else:
			break
	identifier: str = fman.select_identifier(file)
	with open(path.join(glob.progfiles, "lastopen"), 'w') as f:
		f.write(f"{file}.todo\n{identifier}")
	with open(path.join(glob.listfiles, f"{file}.todo"), 'w') as f:
		for items in todo:
			f.write(f"{items}\n")
		f.write(identifier)
	gnrl.slowprint('', f"File written successfully to '{glob.listfiles}/{file}.todo'.", '')
	return None

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

def load(unchanged: list[str]) -> list[str]:
	if not len(listdir(glob.listfiles)):
		gnrl.slowprint('', "No files to show.", '')
		return unchanged
	disp.load_menu()
	while True:
		files = fman.get_file_names()
		open_file = fman.read_open_file()
		select = input(" > ").lower()
		if select.isdigit():
			select = int(select) - 1
			if select in range(len(files)):
				if len(open_file):
					last_saved = fman.open_list(open_file["name"])
					last_saved.pop()
					if unchanged != last_saved:
						fman.prompt_save(unchanged)
				elif len(unchanged):
					fman.prompt_save(unchanged)
				todo = fman.open_list(files[select])
				if not len(todo):
					if fman.empty_file_delete(files[select]):
						continue
					else:
						todo = fman.open_list(files[select])
				with open(path.join(glob.progfiles, "lastopen"), 'w') as f:
					f.write(f"{files[select]}\n{todo[-1]}")
				todo.pop()
				break
			else:
				gnrl.slowprint(glob.invalid_fn)
		else:
			match select:
				case 'c':
					gnrl.slowprint('', "No file loaded.", '')
					return unchanged
				case 'r':	
					fman.rename_load_file(files)
				case 'a':
					fman.archive_load_file(files)
				case 'd':		
					fman.delete_load_file(files)
				case _:
					gnrl.slowprint(glob.invalid_fn)
					continue
			disp.load_menu()
	gnrl.slowprint('', f"File {files[select]} successfully loaded.", '')
	return todo