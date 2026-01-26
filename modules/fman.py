from os import listdir, makedirs, path, remove, rename, system
from time import sleep

import modules.glob as glob
import modules.gnrl as gnrl

def get_file_names() -> list[str]:
	return [f for f in listdir(glob.listfiles) if ".todo" in f]

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
				remove(path.join(glob.listfiles, filename))
				return True
			case 'n':
				with open(path.join(glob.listfiles, filename), 'w') as f:
					if gnrl.is_daily(filename):
						f.write("%d\n")
					else:
						f.write("%c\n")
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
				confirm(files[to_archive], {"type": "archive", "pres-verb": "archive", "past-verb": "archival"})
				sleep(1)
				return None
			else:
				gnrl.slowprint(glob.invalid_fn)
		elif to_rename.lower() == 'c':
			gnrl.slowprint('', "Cancelled archiving.", '')
			sleep(1)
			return None
		else:
			gnrl.slowprint(glob.invalid_fn)

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
			return None
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
				list_to_be_renamed = open_list(files[to_rename])
				if list_to_be_renamed[-1] == "%d":
					new_name += "(D)"
				open_file = read_open_file()
				if len(open_file) and files[to_rename] == open_file["name"]:
					open_file["name"] = f"{new_name}.todo"
					with open(path.join(glob.progfiles, "lastopen"), 'w') as f:
						f.write(f"{open_file["name"]}\n{open_file["lstype"]}\n")
				rename(path.join(glob.listfiles, files[to_rename]), path.join(glob.listfiles, f"{new_name}.todo"))
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
		with open(path.join(glob.listfiles, file), 'r') as f:
			return [line.strip('\n') for line in f.readlines()]

def autoload() -> None:
	glob.todo = []
	open_file = read_open_file()
	if len(open_file):
		if open_file["lstype"] == "%d" and open_file["name"] != f"{glob.date}.todo":
			if f"{glob.date}.todo" in listdir(glob.listfiles):
				with open(path.join(glob.progfiles, "lastopen"), 'w') as f:
					f.write(f"{glob.date}.todo\n%d\n")
				with open(path.join(glob.listfiles, f"{glob.date}.todo"), 'r') as f:
					glob.todo = [line.strip('\n') for line in f.readlines()]
				glob.todo.pop()
			else:
				glob.todo = open_list(open_file["name"])
				glob.todo.pop()
				rm_crossed()
				append_postponed()
				clear_open_file()
			return None
		try:
			with open(path.join(glob.listfiles, open_file["name"]), 'r') as f:
				glob.todo = [line.strip('\n') for line in f.readlines()]
			glob.todo.pop()
		except Exception:
			clear_open_file()
	return None

def rm_crossed() -> None:
	uncrossed = []
	for item in glob.todo:
		if ord(item[1]) != 822:
			uncrossed.append(item)
	glob.todo = uncrossed
	return None

def delete_load_file(files: list[str]) -> None:
	gnrl.slowprint('', "Enter the number corresponding to the file you would like to delete. 'c' to cancel.", '')
	while True:
		to_delete = input(" > ")
		if to_delete.isdigit():
			to_delete = int(to_delete) - 1
			if to_delete in range(len(files)):
				confirm(files[to_delete], {"type": "delete", "pres-verb": "delete", "past-verb": "deletion"})
				sleep(1)
				return None
			else:
				gnrl.slowprint(glob.invalid_fn)
		elif to_delete.lower() == 'c':
			gnrl.slowprint('', "Cancelled file deletion.", '')
			sleep(1)
			return None
		else:
			gnrl.slowprint(glob.invalid_fn)

def confirm(filename: str, function: dict) -> None:
	file_is_open = False
	open_file = read_open_file()
	if len(open_file) and open_file["name"] == filename:
		file_is_open = True
	if file_is_open:	
		gnrl.slowprint('', f"Are you sure you'd like to {function["pres-verb"]} the file '{filename}'? This will also clear your current to-do list. (y/N)", '')
	else:
		gnrl.slowprint('', f"Are you sure you'd like to {function["pres-verb"]} the file '{filename}'? (y/N)", '')
	while True:
		confirmation = input(" > ").lower()
		match confirmation:
			case 'n' | '':
				gnrl.slowprint('', f"{function["past-verb"].capitalize()} of file '{filename}' cancelled.", '')
				return None
			case 'y':
				if file_is_open:
					clear_open_file()
					glob.todo = []	
				if function["type"] == "delete":
					remove(path.join(glob.listfiles, filename))
					gnrl.slowprint('', "File successfully deleted.", '')
				elif function["type"] == "archive":
					rename(path.join(glob.listfiles, filename), path.join(glob.listfiles, "archive", filename))
					gnrl.slowprint('', f"File successfully archived. It can be found again in the '{path.join(glob.listfiles, "archive")}' directory.", '')
				return None
			case _:
				gnrl.slowprint(glob.y_or_n)

def append_postponed() -> None:
	with open(path.join(glob.progfiles, "postpone"), 'r') as f:
		glob.todo += [line.strip('\n') for line in f.readlines()]
	with open(path.join(glob.progfiles, "postpone"), 'w'):
		pass
	return None

def read_open_file() -> dict[str: str]:
	with open(path.join(glob.progfiles, "lastopen"), 'r') as f:
		open_file = [line.strip('\n') for line in f.readlines()]
	if len(open_file):
		return {"name": open_file[0], "lstype": open_file[1]}
	return {}

def clear_open_file() -> None:
	with open(path.join(glob.progfiles, "lastopen"), 'w'):
		return None

def file_integrity() -> None:
	if not path.exists(glob.progfiles):
		makedirs(glob.progfiles)
	if not path.exists(path.join(glob.progfiles, "lastopen")):
		clear_open_file()
	if not path.exists(path.join(glob.progfiles, "postpone")):
		with open(path.join(glob.progfiles, "postpone"), 'w'):
			pass
	if not path.exists(glob.listfiles):
		makedirs(glob.listfiles)
	if not path.exists(path.join(glob.listfiles, "archive")):
		makedirs(path.join(glob.listfiles, "archive"))	
	return None
