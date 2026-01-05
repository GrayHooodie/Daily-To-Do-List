from os import listdir, system

import glob, progfuncs as pf

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
				fman.save(todo)
				sleep(1)
				return None
			case _:
				gnrl.slowprint(glob.y_or_n)

def select_identifier(filename: str) -> str:
	identifier: str = fman.read_list_type(f"{filename}.todo")
	if identifier:
		return identifier
	elif filename == glob.date:
		return "%d"
	else:
		return "%c"

def read_list_type(filename: str) -> str:
	if fman.file_exists(filename):
		return fman.open_list(filename)[-1]
	return ""

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

def autosave(todo: list[str]) -> None:
	open_file = pf.read_open_file()
	if len(open_file):
		last_saved = fman.open_list(open_file["name"])
		last_saved.pop()
		if todo == last_saved:
			return None
	if (len(open_file)) or (f"{glob.date}.todo" not in listdir(glob.listfiles)):
		if not len(open_file):
			files = fman.get_file_names()
			fman.move_old_dailys(files)
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
		fman.prompt_save(todo)
	system("clear")	
	return None

def move_old_dailys(files):
	for f in files:
		if gnrl.is_daily(f.split(ext)[0]):
			fman.archiveit(f)
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
				fman.archiveit(files[to_archive])
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
				fman.renameit(files, to_rename)
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
	gnrl.slowprint('', f"Enter the new name of '{files[to_rename].split(ext)[0]}'. 'c' to cancel.", '')
	while True:
		new_name = input(" > ")
		if new_name.lower() == 'c':
			gnrl.slowprint('', f"Cancelled renaming of '{files[to_rename].split(ext)[0]}'.", '')
			sleep(1)
			return None
		elif len(new_name) > 1:
			if not fman.file_exists(new_name):
				list_to_be_renamed = fman.open_list(f"{files[to_rename]}")
				if list_to_be_renamed[-1] == "%d":
					new_name += "(D)"
				open_file = pf.read_open_file()
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
	files = fman.get_file_names()
	if filename in files:
		return True
	return False

def load(unchanged: list[str]) -> list[str]:
	if not len(listdir(glob.listfiles)):
		gnrl.slowprint('', "No files to show.", '')
		return unchanged
	while True:
		files = fman.get_file_names()
		disp.load_menu()
		open_file = pf.read_open_file()
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
				with open(f"{glob.progfiles}/lastopen", 'w') as f:
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
	gnrl.slowprint('', f"File {files[select]} successfully loaded.", '')
	return todo

def open_list(file: str) -> list[str]:
	if fman.file_exists(file):	
		with open(f"{glob.listfiles}/{file}", 'r') as f:
			return [line.strip('\n') for line in f.readlines()]

def autoload() -> list[str]:
	todo = []
	open_file = pf.read_open_file()
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
				todo = pf.sort_items(todo, True)
				todo = pf.append_postponed(todo)
				pf.clear_open_file()
			return todo
		try:
			with open(f"{glob.listfiles}/{open_file["name"]}", 'r') as f:
				todo = [line.strip('\n') for line in f.readlines()]
			todo.pop()
		except Exception:
			pf.clear_open_file()
	return todo

def save(todo: list[str]) -> None:
	disp.save_menu()
	files = get_file_names()
	open_file = pf.read_open_file()
	while True:
		file: str = input(" > ")
		if file.isdigit():
			file: int = int(file) - 1
			if file in range(len(files)):
				if overwrite_save(files[file]):
					file: str = files[file].split(ext)[0]
					break
			else:
				gnrl.slowprint("Please enter a valid file number, or name your file.")
		elif file == '':
			if len(open_file):
				file: str = open_file["name"].split(ext)[0]
				break
			elif f"{glob.date}.todo" not in files:
				file: str = glob.date
				move_old_dailys(files)
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
	identifier: str = select_identifier(file)
	with open(f"{glob.progfiles}/lastopen", 'w') as f:
		f.write(f"{file}.todo\n{identifier}")
	with open(f"{glob.listfiles}/{file}.todo", 'w') as f:
		for items in todo:
			f.write(f"{items}\n")
		f.write(identifier)
	gnrl.slowprint('', f"File written successfully to '{glob.listfiles}/{file}.todo'.", '')
	return None

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
				open_file = pf.read_open_file()
				if len(open_file) and open_file["name"] == files[to_delete]:
					pf.clear_open_file()
				remove(f"{glob.listfiles}/{files[to_delete]}")
				return None
			case _:
				gnrl.slowprint(glob.y_or_n)

