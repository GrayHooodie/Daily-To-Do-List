from os import listdir, remove, rename, system
from time import sleep

import modules.glob as glob
import modules.gnrl as gnrl

def get_file_names() -> list[str]:
	files = listdir(glob.listfiles)
	num = 1
	for i in range(len(files)):
		if i >= len(files):
			break
		if glob.ext not in files[i]:
			files.remove(files[i])
		num += 1
	return files

def prompt_save(todo) -> None:
	gnrl.slowprint('', "Would you like to save your current to-do list? (Y/n)", '')
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
				gnrl.slowprint(glob.y_or_n)

def select_identifier(filename: str) -> str:
	identifier: str = read_list_type(f"{filename}.todo")
	if identifier:
		return identifier
	elif filename == glob.date:
		return "%d"
	else:
		return "%c"

def read_list_type(filename: str) -> str:
	if file_exists(filename):
		return open_list(filename)[-1]
	return ""

def autosave(todo: list[str]) -> None:
	open_file = read_open_file()
	if len(open_file):
		last_saved = open_list(open_file["name"])
		last_saved.pop()
		if todo == last_saved:
			return None
	if (len(open_file)) or (f"{glob.date}.todo" not in listdir(glob.listfiles)):
		if not len(open_file):
			files = get_file_names()
			move_old_dailys(files)
			open_file = {"name": f"{glob.date}.todo", "lstype": "%d"}
			with open(f"{glob.progfiles}/lastopen", 'w') as f:
				f.write(f"{open_file["name"]}\n{open_file["lstype"]}")	
		with open(f"{glob.listfiles}/{open_file["name"]}", 'w') as f:
			for items in todo:
				f.write(f"{items}\n")
			f.write(f"{open_file["lstype"]}")
		gnrl.slowprint('', f"Saved list to '{open_file["name"]}'.", '')
		sleep(1)
	else:
		prompt_save(todo)
	return None

def move_old_dailys(files):
	for f in files:
		if gnrl.is_daily(f.split(glob.ext)[0]):
			archiveit(f)
	return None

def empty_file_delete(filename: str) -> bool:
	gnrl.slowprint('', "The file you're trying to open is empty. Would you like to delete it? 'y' to delete, and 'n' to open. (y/n)", '')
	while True:
		will_delete = input(" > ").lower()
		match will_delete:
			case 'y':
				remove(f"{glob.listfiles}/{filename}")
				return True
			case 'n':
				with open(f"{glob.listfiles}/{filename}", 'w') as f:
					if gnrl.is_daily(filename):
						f.write("%d")
					else:
						f.write("%c")
				return False
			case _:
				gnrl.slowprint(glob.y_or_n)

def archive_load_file(files: list[str]) -> None:
	gnrl.slowprint('', "Enter the number corresponding to the file you would like to archive. 'c' to cancel.", '')
	while True:
		to_archive = input(" > ")
		if to_archive.isdigit():
			to_archive = int(to_archive) - 1
			if to_archive in range(len(files)):
				archiveit(files[to_archive])
				return None
			else:
				gnrl.slowprint(glob.invalid_fn)
		elif to_rename.lower() == 'c':
			gnrl.slowprint('', "Cancelled archiving.", '')
			sleep(1)
			return 
		else:
			gnrl.slowprint(glob.invalid_fn)

def archiveit(filename: str) -> None:
	rename(f"{glob.listfiles}/{filename}", f"{glob.listfiles}/archive/{filename}")
	return None

def rename_load_file(files: list[str]) -> None:
	gnrl.slowprint('', "Enter the number corresponding to the file you would like to rename. 'c' to cancel.", '')
	while True:
		to_rename = input(" > ")
		if to_rename.isdigit():
			to_rename = int(to_rename) - 1
			if to_rename in range(len(files)):
				renameit(files, to_rename)
				return None
			else:
				gnrl.slowprint(glob.invalid_fn)
		elif to_rename.lower() == 'c':
			gnrl.slowprint('', "Cancelled renaming.", '')
			sleep(1)
			return 
		else:
			gnrl.slowprint(glob.invalid_fn)

def renameit(files, to_rename) -> None:
	gnrl.slowprint('', f"Enter the new name of '{files[to_rename].split(glob.ext)[0]}'. 'c' to cancel.", '')
	while True:
		new_name = input(" > ")
		if new_name.lower() == 'c':
			gnrl.slowprint('', f"Cancelled renaming of '{files[to_rename].split(glob.ext)[0]}'.", '')
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
					with open(f"{glob.progfiles}/lastopen", 'w') as f:
						f.write(f"{open_file["name"]}\n{open_file["lstype"]}")
				rename(f"{glob.listfiles}/{files[to_rename]}", f"{glob.listfiles}/{new_name}.todo")
				return None
			else:
				gnrl.slowprint(f"Name '{new_name}' already in use. If you wish to use the name '{new_name}' for this file, first delete the file currently using that name.")
		else:
			gnrl.slowprint("Name must be longer than one character.")

def file_exists(filename: str) -> bool:
	files = get_file_names()
	if filename in files:
		return True
	return False

def open_list(file: str) -> list[str]:
	if file_exists(file):	
		with open(f"{glob.listfiles}/{file}", 'r') as f:
			return [line.strip('\n') for line in f.readlines()]

def autoload() -> list[str]:
	todo = []
	open_file = read_open_file()
	if len(open_file):
		if open_file["lstype"] == "%d" and open_file["name"] != f"{glob.date}.todo":
			if f"{glob.date}.todo" in listdir(glob.listfiles):
				with open(f"{glob.progfiles}/lastopen", 'w') as f:
					f.write(f"{glob.date}.todo\n%d")
				with open(f"{glob.listfiles}/{glob.date}.todo", 'r') as f:
					todo = [line.strip('\n') for line in f.readlines()]
				todo.pop()
			else:
				todo = open_list(open_file["name"])
				todo.pop()
				todo = rm_crossed(todo)
				todo = append_postponed(todo)
				clear_open_file()
			return todo
		try:
			with open(f"{glob.listfiles}/{open_file["name"]}", 'r') as f:
				todo = [line.strip('\n') for line in f.readlines()]
			todo.pop()
		except Exception:
			clear_open_file()
	return todo

def rm_crossed(todo: list[str]) -> list[str]:
	uncrossed = []
	for item in todo:
		if ord(item[1]) != 822:
			uncrossed.append(item)
	return uncrossed

def delete_load_file(files: list[str]) -> None:
	gnrl.slowprint('', "Enter the number corresponding to the file you would like to delete. 'c' to cancel.", '')
	while True:
		to_delete = input(" > ")
		if to_delete.isdigit():
			to_delete = int(to_delete) - 1
			if to_delete in range(len(files)):
				confirm_delete(files, to_delete)
				return None
			else:
				gnrl.slowprint(glob.invalid_fn)
		elif to_delete.lower() == 'c':
			gnrl.slowprint('', "Cancelled file deletion.", '')
			sleep(1)
			return None
		else:
			gnrl.slowprint(glob.invalid_fn)

def confirm_delete(files: list[str], to_delete: int) -> None:
	gnrl.slowprint('', f"Are you sure you'd like to delete the file '{files[to_delete]}'? (y/N)", '')
	while True:
		confirm_delete = input(" > ").lower()
		match confirm_delete:
			case 'n' | '':
				gnrl.slowprint('', f"Deletion of file '{files[to_delete]}' cancelled.", '')
				sleep(1)
				return None
			case 'y':
				open_file = read_open_file()
				if len(open_file) and open_file["name"] == files[to_delete]:
					clear_open_file()
				remove(f"{glob.listfiles}/{files[to_delete]}")
				return None
			case _:
				gnrl.slowprint(glob.y_or_n)

def append_postponed(todo: list[str]) -> list[str]:
	with open(f"{glob.progfiles}/postpone", 'r') as f:
		todo += [line.strip('\n') for line in f.readlines()]
	with open(f"{glob.progfiles}/postpone", 'w'):
		pass
	return todo

def read_open_file() -> dict[str: str]:
	with open(f"{glob.progfiles}/lastopen", 'r') as f:
		open_file = [line.strip('\n') for line in f.readlines()]
	if len(open_file):
		return {"name": open_file[0], "lstype": open_file[1]}
	return {}

def clear_open_file() -> None:
	with open(f"{glob.progfiles}/lastopen", 'w'):
		return None