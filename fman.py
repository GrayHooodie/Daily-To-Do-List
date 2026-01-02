from os import listdir

import dtdl, glob, disp, lman

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

def add_to_postpone(to_postpone: list[str]) -> None:
	with open(f"{progfiles}/postpone", 'a') as f:
		for item in to_postpone:
			f.write(f"{item}\n")	
	return None

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

def save(todo: list[str]) -> None:
	disp.save_menu()
	files = fman.get_file_names()
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

 