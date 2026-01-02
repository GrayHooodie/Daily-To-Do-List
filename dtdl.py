# Simple todo-list program made by Matt L on 2025/12/11 while not wanting to go to sleep

from datetime import datetime
from time import sleep
from os import system, path, makedirs, listdir, getlogin, rename, remove

usr: str = getlogin()
date: str = datetime.today().strftime('%Y-%m-%d')

listfiles: str = f"/home/{usr}/Documents/To-Do Lists"
progfiles: str = f"/home/{usr}/.todolist/programfiles"
ext: str = ".todo"

invalid_ln: str = "Please enter a valid line number."
invalid_fn: str = "Please enter a valid file number."
y_or_n: str = "Enter 'y' or 'n'."
no_chng: str = "No changes made."

# ==================== functions =====================


def list_items(todo: list[str]) -> None:
	open_file = read_open_file()
	if len(open_file):
		slowprint(f"Current File: {open_file["name"]}")
	slowprint('', "To-Do List:", '')
	if len(todo) > 0:
		num = 1
		for item in todo:
			if num < 10:
				slowprint(f" {num}.  {item}")
			else:
				slowprint(f" {num}. {item}")
			num += 1
	else:
		slowprint(" (Empty)")
	slowprint('')
	return None

def get_file_names() -> list[str]:
	files = listdir(listfiles)
	num = 1
	for i in range(len(files)):
		if i >= len(files):
			break
		if ext not in files[i]:
			files.remove(files[i])
		num += 1
	return files

def list_files(*function_header: str) -> list[str]:
	open_file = read_open_file()
	if len(open_file):
		disp_open_file = f"\nCurrent File: {open_file["name"]}"
	else:
		disp_open_file = ''
	slowprint(function_header[0], function_header[1], f"{disp_open_file}", '', "Files:", '')
	files = get_file_names()
	num = 1
	for file in files:
		if num < 10:
			slowprint(f" {num}.  {file}")
		else:
			slowprint(f" {num}. {file}")
		num += 1
	slowprint('')	
	return files

def sort_items(todo: list[str], transfer: bool) -> list[str]:
	uncrossed = []
	crossed = []
	for item in todo:
		if ord(item[1]) == 822:
			crossed.append(item)
		else:
			uncrossed.append(item)
	if transfer:
		return uncrossed	
	return uncrossed + crossed

def cross(todo: list[str], line: int) -> list[str]:
	if ord(todo[line][1]) == 822:
		todo[line] = unstrike(todo[line])
	else:
		todo[line] = strike(todo[line])
	return todo

def enter_digit(base: int, length: int, text: list[str], enter_to_confirm: bool) -> int:
	slowprint('', text[0], '')
	while True:
		num = input(" > ")
		if num.isdigit():
			num = int(num) - base
			if num in range(length):
				return num
		elif num.lower() == 'c':
			if len(text) == 3:
				slowprint('', text[2], '')
			return -2
		elif enter_to_confirm and num == '':
			return -1	
		slowprint(text[1])
		
def confirm_edits(is_equal: bool, function: str) -> None:
	if is_equal:
		slowprint('', no_chng, '')
	else:
		slowprint('', f"Item(s) successfully {function}.", '')
	return None
			
def arrange_items_menu(todo: list[str]) -> None:
	system("clear")
	slowprint("[arranging items]", "-----------------", '')
	list_items(todo)
	return None

def arrange_items(todo: list[str]) -> list[str]:
	unchanged = todo.copy()
	arrange_items_menu(todo)
	first_text = ["Enter the line number you would like to move. Empty return to finish arranging items. 'c' to cancel.", invalid_ln]
	while True:
		line = enter_digit(1, len(todo), first_text, True)
		if line == -1:
			confirm_edits(todo == unchanged, "arranged")
			return todo
		elif line == -2:
			slowprint('', no_chng, '')
			return unchanged
		second_text = [f"Enter the new position of line {line + 1}. 'c' to cancel line {line + 1} arrangement.", invalid_ln, f"Cancelled arrangement of line {line + 1}."]
		dest = enter_digit(1, len(todo), second_text, False)
		if dest == -2:
			sleep(1)
			arrange_items_menu(todo)
			continue
		item = todo[line]
		todo.remove(item)
		todo.insert(dest, item)
		arrange_items_menu(todo)

def edit_items_menu(todo: list[str]) -> None:
	system("clear")
	slowprint("[editing items]", "---------------", '')
	list_items(todo)
	return None

def edit_items(todo: list[str]) -> list[str]:
	unchanged = todo.copy()
	edit_items_menu(todo)
	first_text = ["Enter the line number you would like to edit. Empty return to finish editing items. 'c' to cancel.", invalid_ln]
	while True:
		line = enter_digit(1, len(todo), first_text, True)
		if line == -1:
			confirm_edits(todo == unchanged, 'edited')
			return todo
		elif line == -2:
			slowprint('', no_chng, '')
			return unchanged
		second_text = [f"Enter the new text for line {line + 1}. 'c' to cancel edits on line {line + 1}.", "Item can't be a number.", f"Cancelled edits on line {line + 1}", "Item must be two or more characters."]
		edited = edit_item_text(2, second_text)
		if edited == 'c':
			sleep(1)
			edit_items_menu(todo)	
			continue
		todo.remove(todo[line])
		todo.insert(line, edited)
		edit_items_menu(todo)

def edit_item_text(minlength: int, text: list[str]) -> str:
	slowprint('', text[0], '')
	while True:
		edited = input(" > ")
		if edited.isdigit():
			slowprint(text[1])
			continue
		elif len(edited) >= minlength:
			return edited
		elif edited.lower() == 'c':
			slowprint('', text[2], '')
			return edited
		slowprint(text[3])

def postpone_items_menu(todo: list[str]) -> None:
	system("clear")
	slowprint("[postponing items]", "------------------", '')
	list_items(todo)
	return None

def postpone_items(todo: list[str]) -> list[str]:
	open_file = read_open_file()
	if not len(open_file):
		slowprint("Must have a file open to postpone items.")
		return todo
	elif open_file["lstype"] == "%c":
		slowprint("File must be a 'daily' to-do list to postpone items.")
		return todo
	unchanged = todo.copy()
	to_postpone = []
	text = ["Enter line number(s) to postpone. Empty return to finish postponing items. 'c' to cancel.", invalid_ln]
	while True:
		postpone_items_menu(todo)
		line = enter_digit(1, len(todo), text, True)
		if line == -1:
			break
		elif line == -2:
			slowprint('', no_chng, '')
			return unchanged
		to_postpone.append(todo[line])	
		todo.remove(todo[line])
	add_to_postpone(to_postpone)	
	confirm_edits(todo == unchanged, "postponed")	
	return todo
			
def add_to_postpone(to_postpone: list[str]) -> None:
	with open(f"{progfiles}/postpone", 'a') as f:
		for item in to_postpone:
			f.write(f"{item}\n")	
	return None

def rm_items_menu(todo: list[str]) -> None:
	system("clear")
	slowprint("[removing items]", "----------------", '')
	list_items(todo)
	return None

def rm_items(todo: list[str]) -> list[str]:
	unchanged = todo.copy()
	text = ["Enter line number(s) to remove. Empty return to finish removing items. 'c' to cancel.", invalid_ln]
	while True:
		rm_items_menu(todo)
		line = enter_digit(1, len(todo), text, True)
		if line == -1:
			confirm_edits(todo == unchanged, "removed")	
			if not len(todo):
				clear_open_file()	
			return todo
		elif line == -2:
			slowprint('', no_chng, '')
			return unchanged
		todo.pop(line)

def clear(todo):
	slowprint('', "Are you sure you want to clear your to-do list? (y/N)", '')
	while True:
		check = input(" > ")
		match check:
			case 'y' | 'Y':
				clear_open_file()
				slowprint('', "To-do list cleared.", '')
				return []
			case 'n' | 'N' | '':
				slowprint('', no_chng, '')
				return todo 
			case _:
				slowprint(y_or_n)

def prompt_save(todo) -> None:
	slowprint('', "Would you like to save your current to-do list? (Y/n)", '')
	while True:
		will_save = input(" > ")
		match will_save:
			case 'n' | 'N':
				return None
			case 'y' | 'Y' | '':
				save(todo)
				sleep(1)
				return None
			case _:
				slowprint(y_or_n)

def save_menu():
	system("clear")
	open_file = read_open_file()
	files = list_files("[saving file]", "-------------")
	if len(open_file) and file_exists(open_file["name"]):
		slowprint('', f"Name your file, or empty return to overwrite '{open_file["name"]}'. 'c' to cancel.", '')
	elif f"{date}.todo" not in files:
		slowprint('', f"Name your file, or empty return to name the file '{date}'. 'c' to cancel.", '')
	else:
		slowprint('', "Name your file, or enter the corresponding number to overwrite a file. 'c' to cancel.", '')
	return files

def save(todo: list[str]) -> None:
	files: list[str] = save_menu()
	open_file = read_open_file()
	while True:
		file: str = input(" > ")
		if file.isdigit():
			file: int = int(file) - 1
			if file in range(len(files)):
				if overwrite_save(files[file]):
					file: str = files[file].split(ext)[0]
					break
			else:
				slowprint("Please enter a valid file number, or name your file.")
		elif file == '':
			if len(open_file):
				file: str = open_file["name"].split(ext)[0]
				break
			elif f"{date}.todo" not in files:
				file: str = date
				move_old_dailys(files)
				break
			else:
				slowprint("Please name your file.")
		elif file == 'c':
			slowprint('', "Cancelled file save.", '')
			return
		elif is_daily(file):
			slowprint("Name can't be a date in the format of 'YYYY-MM-DD'.")
		elif f"{file}.todo" in files:
			if overwrite_save(f"{file}.todo"):
				break
		elif ext in file:
			slowprint("Name can't contain '.todo'.")
		else:
			break
	identifier: str = select_identifier(file)
	with open(f"{progfiles}/lastopen", 'w') as f:
		f.write(f"{file}.todo\n{identifier}")
	with open(f"{listfiles}/{file}.todo", 'w') as f:
		for items in todo:
			f.write(f"{items}\n")
		f.write(identifier)
	slowprint('', f"File written successfully to '{listfiles}/{file}.todo'.", '')
	return None

def select_identifier(filename: str) -> str:
	identifier: str = read_list_type(f"{filename}.todo")
	if identifier:
		return identifier
	elif filename == date:
		return "%d"
	else:
		return "%c"

def is_daily(file: str) -> bool:
	isdate = file.split('-')
	if len(isdate) == 3:
		for i in range(len(isdate)):
			if not isdate[i].isdigit():
				return False
			else:
				isdate[i] = int(isdate[i])
		if isdate[0] in range(2000, 10000) and isdate[1] in range(1, 32) and isdate[2] in range(1, 32):
			return True
	return False

def read_list_type(filename: str) -> str:
	if file_exists(filename):
		return open_list(filename)[-1]
	return ""

def overwrite_save(filename: str) -> bool:
	slowprint('', f"'{filename}' already exists. Would you like to overwrite it? (y/N)", '')
	while True:
		will_overwrite = input(" > ")
		match will_overwrite:
			case 'n' | 'N' | '':
				save_menu()
				return False
			case 'y' | 'Y':
				return True
			case _:
				slowprint(y_or_n)

def autosave(todo: list[str]) -> None:
	open_file = read_open_file()
	if len(open_file):
		last_saved = open_list(open_file["name"])
		last_saved.pop()
		if todo == last_saved:
			return None
	if (len(open_file)) or (f"{date}.todo" not in listdir(listfiles)):
		if not len(open_file):
			files = get_file_names()
			move_old_dailys(files)
			open_file = {"name": f"{date}.todo", "lstype": "%d"}
			with open(f"{progfiles}/lastopen", 'w') as f:
				f.write(f"{open_file["name"]}\n{open_file["lstype"]}")	
		with open(f"{listfiles}/{open_file["name"]}", 'w') as f:
			for items in todo:
				f.write(f"{items}\n")
			f.write(f"{open_file["lstype"]}")
		slowprint('', f"Saved list to '{open_file["name"]}'.", '')
		sleep(1)
	else:
		prompt_save(todo)
	return None

def move_old_dailys(files):
	for f in files:
		if is_daily(f.split(ext)[0]):
			archive(f)
	return None

def load_menu() -> list[str]:
	system("clear")
	files = list_files("[loading file]", "--------------")
	slowprint('', "Enter the number of file you would like to open. 'r' to rename a file. 'd' to delete a file. 'a' to archive a file. 'c' to cancel.", '')
	return files

def load(unchanged: list[str]) -> list[str]:
	if not len(listdir(listfiles)):
		slowprint('', "No files to show.", '')
		return unchanged
	files = load_menu()
	while True:
		open_file = read_open_file()
		select = input(" > ").lower()
		if select.isdigit():
			select = int(select) - 1
			if select in range(len(files)):
				if len(open_file):
					last_saved = open_list(open_file["name"])
					last_saved.pop()
					if unchanged != last_saved:
						prompt_save(unchanged)
				elif len(unchanged):
					prompt_save(unchanged)
				todo = open_list(files[select])
				if not len(todo):
					if empty_file_delete(files[select]):
						files = load_menu()
						continue
					else:
						todo = open_list(files[select])
				with open(f"{progfiles}/lastopen", 'w') as f:
					f.write(f"{files[select]}\n{todo[-1]}")
				todo.pop()
				break
			else:
				slowprint(invalid_fn)
		else:
			match select:
				case 'c':
					slowprint('', "No file loaded.", '')
					return unchanged
				case 'r':	
					rename_load_file(files)
					files = load_menu()
				case 'a':
					archive_load_file(files)
					files = load_menu()
				case 'd':		
					delete_load_file(files)
					files = load_menu()
				case _:
					slowprint(invalid_fn)
	slowprint('', f"File {files[select]} successfully loaded.", '')
	return todo

def empty_file_delete(filename: str) -> bool:
	slowprint('', "The file you're trying to open is empty. Would you like to delete it? 'y' to delete, and 'n' to open. (y/n)", '')
	while True:
		will_delete = input(" > ").lower()
		match will_delete:
			case 'y':
				remove(f"{listfiles}/{filename}")
				return True
			case 'n':
				with open(f"{listfiles}/{filename}", 'w') as f:
					if is_daily(filename):
						f.write("%d")
					else:
						f.write("%c")
				return False
			case _:
				slowprint(y_or_n)

def open_list(file: str) -> list[str]:
	if file_exists(file):	
		with open(f"{listfiles}/{file}", 'r') as f:
			return [line.strip('\n') for line in f.readlines()]

def archive_load_file(files: list[str]) -> None:
	slowprint('', "Enter the number corresponding to the file you would like to archive. 'c' to cancel.", '')
	while True:
		to_archive = input(" > ")
		if to_archive.isdigit():
			to_archive = int(to_archive) - 1
			if to_archive in range(len(files)):
				archive(files[to_archive])
				return None
			else:
				slowprint(invalid_fn)
		elif to_rename.lower() == 'c':
			slowprint('', "Cancelled archiving.", '')
			sleep(1)
			return 
		else:
			slowprint(invalid_fn)

def archive(filename: str) -> None:
	rename(f"{listfiles}/{filename}", f"{listfiles}/archive/{filename}")
	return None

def rename_load_file(files: list[str]) -> None:
	slowprint('', "Enter the number corresponding to the file you would like to rename. 'c' to cancel.", '')
	while True:
		to_rename = input(" > ")
		if to_rename.isdigit():
			to_rename = int(to_rename) - 1
			if to_rename in range(len(files)):
				new_name(files, to_rename)
				return None
			else:
				slowprint(invalid_fn)
		elif to_rename.lower() == 'c':
			slowprint('', "Cancelled renaming.", '')
			sleep(1)
			return 
		else:
			slowprint(invalid_fn)

def new_name(files, to_rename) -> None:
	slowprint('', f"Enter the new name of '{files[to_rename].split(ext)[0]}'. 'c' to cancel.", '')
	while True:
		new_name = input(" > ")
		if new_name.lower() == 'c':
			slowprint('', f"Cancelled renaming of '{files[to_rename].split(ext)[0]}'.", '')
			sleep(1)
			return None
		elif len(new_name) > 1:
			if not file_exists(new_name):
				list_to_be_renamed = open_list(f"{files[to_rename]}")
				if list_to_be_renamed[-1] == "%d":
					new_name += "(D)"
				open_file = read_open_file()
				if len(open_file) and files[to_rename] == open_file["name"]:
					open_file["name"] = f"{new_name}.todo"
					with open(f"{progfiles}/lastopen", 'w') as f:
						f.write(f"{open_file["name"]}\n{open_file["lstype"]}")
				rename(f"{listfiles}/{files[to_rename]}", f"{listfiles}/{new_name}.todo")
				return None
			else:
				slowprint(f"Name '{new_name}' already in use. If you wish to use the name '{new_name}' for this file, first delete the file currently using that name.")
		else:
			slowprint("Name must be longer than one character.")

def delete_load_file(files: list[str]) -> None:
	slowprint('', "Enter the number corresponding to the file you would like to delete. 'c' to cancel.", '')
	while True:
		to_delete = input(" > ")
		if to_delete.isdigit():
			to_delete = int(to_delete) - 1
			if to_delete in range(len(files)):
				confirm_delete(files, to_delete)
				return None
			else:
				slowprint(invalid_fn)
		elif to_delete.lower() == 'c':
			slowprint('', "Cancelled file deletion.", '')
			sleep(1)
			return None
		else:
			slowprint(invalid_fn)

def confirm_delete(files: list[str], to_delete: int) -> None:
	slowprint('', f"Are you sure you'd like to delete the file '{files[to_delete]}'? (y/N)", '')
	while True:
		confirm_delete = input(" > ").lower()
		match confirm_delete:
			case 'n' | '':
				slowprint('', f"Deletion of file '{files[to_delete]}' cancelled.", '')
				sleep(1)
				return None
			case 'y':
				open_file = read_open_file()
				if len(open_file) and open_file["name"] == files[to_delete]:
					clear_open_file()
				remove(f"{listfiles}/{files[to_delete]}")
				return None
			case _:
				slowprint(y_or_n)
							
def autoload() -> list[str]:
	todo = []
	open_file = read_open_file()
	if len(open_file):
		if open_file["lstype"] == "%d" and open_file["name"] != f"{date}.todo":
			if f"{date}.todo" in listdir(listfiles):
				with open(f"{progfiles}/lastopen", 'w') as f:
					f.write(f"{date}.todo\n%d")
				with open(f"{listfiles}/{date}.todo", 'r') as f:
					todo = [line.strip('\n') for line in f.readlines()]
				todo.pop()
			else:
				todo = open_list(open_file["name"])
				todo.pop()
				todo = sort_items(todo, True)
				todo = append_postponed(todo)
				clear_open_file()
			return todo
		try:
			with open(f"{listfiles}/{open_file["name"]}", 'r') as f:
				todo = [line.strip('\n') for line in f.readlines()]
			todo.pop()
		except Exception:
			clear_open_file()
	return todo

def append_postponed(todo: list[str]) -> list[str]:
	with open(f"{progfiles}/postpone", 'r') as f:
		todo += [line.strip('\n') for line in f.readlines()]
	with open(f"{progfiles}/postpone", 'w'):
		pass
	return todo

def file_integrity() -> None:
	if not path.exists(progfiles):
		makedirs(progfiles)
	if not path.exists(f"{progfiles}/lastopen"):
		clear_open_file()
	if not path.exists(f"{progfiles}/postpone"):
		with open(f"{progfiles}/postpone", 'w'):
			pass
	if not path.exists(listfiles):
		makedirs(listfiles)
	if not path.exists(f"{listfiles}/archive"):
		makedirs(f"{listfiles}/archive")	
	return None

def file_exists(filename: str) -> bool:
	files = get_file_names()
	if filename in files:
		return True
	return False

def read_open_file() -> dict[str: str]:
	with open(f"{progfiles}/lastopen", 'r') as f:
		open_file = [line.strip('\n') for line in f.readlines()]
	if len(open_file):
		return {"name": open_file[0], "lstype": open_file[1]}
	return {}

def clear_open_file() -> None:
	with open(f"{progfiles}/lastopen", 'w'):
		return None

def title() -> None:
	system("clear")
	slowprint('', "---------------------------", "Welcome to your to-do list!", "---------------------------", '')
	return None

def strike(text: str) -> str:
	new_text: str = ""
	for c in text:
		new_text += c + '\u0336'
	return new_text

def unstrike(text: str) -> str:
	new_text: str = ""
	for i in range(0, len(text), 2):
		new_text += text[i]
	return new_text

def slowprint(*text) -> None:
	delay: float = 0.02
	for line in text:
		print(line)
		sleep(delay)
	return None

# display edit menu title
def menu(todo: list[str], justopened: bool) -> None:
	system("clear")
	if justopened:
		title()
	list_items(todo)
	slowprint('', "Add an item, or cross-off an item by entering its line number. 'h' for help.", '')
	return None

# returning to the edit menu from another function
def return_to_menu(todo: list[str]) -> None:
	sleep(1)
	menu(todo, False)
	return None


# ======================== functions ===========================

def main():
	file_integrity()
	todo: list[str] = autoload()
	menu(todo, True)
	while True:
		item: str = input(" > ")
		if item.isdigit():
			item: int = int(item) - 1
			if item in range(len(todo)):
				cross(todo, item)		
				menu(todo, False)
			else:
				slowprint("Please enter a valid line number to cross-off.")
		else:
			match item:
				case '':
					menu(todo, False)
				case 's':
					todo: list[str] = sort_items(todo, False)
					menu(todo, False)
				case 'a' | 'A':
					if len(todo) > 1:
						todo: list[str] = arrange_items(todo)
						return_to_menu(todo)
					else:
						slowprint("Must have at least 2 list items to arrange.")
				case 'e' | 'E':
					if len(todo) > 0:
						todo: list[str] = edit_items(todo)
						return_to_menu(todo)
					else:
						slowprint("Must have at least 1 list item to edit.")
				case 'p' | 'P':
					todo = postpone_items(todo)
					return_to_menu(todo)	
				case 'r' | 'R':
					if len(todo) > 0:
						todo: list[str] = rm_items(todo)
						return_to_menu(todo)
					else:
						slowprint("Must have at least 1 list item to remove.")
				case 'c' | 'C':
					todo: list[str] = clear(todo)
					return_to_menu(todo)
				case 'S':
					if len(todo) > 0:
						save(todo)
						return_to_menu(todo)
					else:
						slowprint("Must have a list to save.")
				case 'l' | 'L':
					todo: list[str] = load(todo)
					return_to_menu(todo)
				case 'h' | 'H':
					slowprint('', "'s'  Sort Items", "'a'  Arrange Items", "'e'  Edit Items", "'p'  Postpone Items", "'r'  Remove Items", '', "'C'  Clear List", "'S'  Save List To File", "'L'  Load List From File", '', "'h'  Show This Help Text", "'q'  Quit", '')
				case 'q' | 'Q':
					if len(todo):
						autosave(todo)
					system("clear")
					return 0
				case _:
					if len(item) > 1:
						todo.append(item)
						menu(todo, False)
					else:
						slowprint(f"Unknown command '{item}'.") 

if __name__ == "__main__":
	main()
