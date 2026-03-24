from os import listdir, path, remove, rename
from time import sleep

# Local modules imports
import modules.glob as glob
import modules.gnrl as gnrl

# Get names of every to-do list
def get_file_names() -> list[str]:
	return [f for f in listdir(glob.LISTFILES) if ".todo" in f]

# Get which type of list, from a filename w/o the extension
def select_identifier(filename: str) -> str:
	if file_exists(f"{filename}.todo"):
		return open_list(f"{filename}.todo")[-1]
	elif gnrl.is_daily(filename):
		return "%d"
	else:
		return "%c"

# Archive old dailys after saving today's to-do list
def move_old_dailys(files):
	for f in files:
		fstripped = f.split(glob.EXT)[0]
		if gnrl.is_daily(fstripped) and fstripped != glob.date:
			archiveit(f)
	return None

# Handle empty/nonexistant files
def empty_file_delete(filename: str) -> bool:
	gnrl.slowprint('', "The file you're trying to open is empty. Would you like to delete it? 'y' to delete, and 'n' to open. (y/n)", '')
	while True:
		will_delete = input(" > ").lower()
		match will_delete:
			case 'y':
				try:
					remove(path.join(glob.LISTFILES, filename))
				except FileNotFoundError:
					pass
				return True
			case 'n':
				with open(path.join(glob.LISTFILES, filename), 'w') as f:
					if gnrl.is_daily(filename):
						f.write("%d\n")
					else:
						f.write("%c\n")
				return False
			case _:
				gnrl.slowprint(glob.Y_OR_N)

# Child user-interactive function
def archive_load_file(files: list[str]) -> None:
	gnrl.slowprint('', "Enter the number corresponding to the file you would like to archive. 'c' to cancel.", '')
	while True:
		to_archive = input(" > ")
		if to_archive.isdigit():
			to_archive = int(to_archive) - 1
			if to_archive in range(len(files)):
				confirm(files[to_archive], {'type': "archive", 'pres-verb': "archive", 'past-verb': "archival"})
				sleep(glob.SLPTM)
				return None
			else:
				gnrl.slowprint(glob.INV_FUNC)
		elif to_archive.lower() == 'c':
			gnrl.slowprint('', "Cancelled archiving.", '')
			sleep(glob.SLPTM)
			return None
		else:
			gnrl.slowprint(glob.INV_FUNC)

# Break down parent function ^
def archiveit(filename: str) -> None:
	rename(path.join(glob.LISTFILES, filename), path.join(glob.LISTFILES, "archive", filename))
	return None

# Child user-interactive function
def rename_load_file(files: list[str]) -> None:
	gnrl.slowprint('', "Enter the number corresponding to the file you would like to rename. 'c' to cancel.", '')
	while True:
		to_rename = input(" > ")
		if to_rename.isdigit():
			to_rename = int(to_rename) - 1
			if to_rename in range(len(files)):
				if gnrl.is_daily(files[to_rename].split(glob.EXT)[0]):
					gnrl.slowprint("Can't rename a daily list.")
					continue	
				renameit(files, to_rename)
				return None
			else:
				gnrl.slowprint(glob.INV_FUNC)
		elif to_rename.lower() == 'c':
			gnrl.slowprint('', "Cancelled renaming.", '')
			sleep(glob.SLPTM)
			return None
		else:
			gnrl.slowprint(glob.INV_FUNC)

# Break down parent function ^
def renameit(files, to_rename) -> None:
	gnrl.slowprint('', f"Enter the new name of '{files[to_rename].split(glob.EXT)[0]}'. 'c' to cancel.", '')
	while True:
		new_name = input(" > ")
		if new_name.lower() == 'c':
			gnrl.slowprint('', f"Cancelled renaming of '{files[to_rename].split(glob.EXT)[0]}'.", '')
			sleep(glob.SLPTM)
			return None
		elif len(new_name) > 0:
			if not file_exists(new_name):
				open_file = read_open_file()
				if len(open_file) and files[to_rename] == open_file['name']:
					open_file['name'] = f"{new_name}.todo"
					with open(path.join(glob.PROGFILES, "lastopen"), 'w') as f:
						f.write(f"{open_file['name']}\n{open_file['type']}\n")
				rename(path.join(glob.LISTFILES, files[to_rename]), path.join(glob.LISTFILES, f"{new_name}.todo"))
				return None
			else:
				gnrl.slowprint(f"Name '{new_name}' already in use. If you wish to use the name '{new_name}' for this file, first delete the file currently using that name.")
		else:
			gnrl.slowprint("Name must be at least one character long.")

# Find whether a to-do list exists or not
def file_exists(filename: str) -> bool:
	files = get_file_names()
	if filename in files:
		return True
	return False

# Open an available to-do list
def open_list(file: str) -> list[str]:
	if file_exists(file):	
		with open(path.join(glob.LISTFILES, file), 'r') as f:
			return [line.strip('\n') for line in f.readlines()]
	else:
		return []

# Autoload the last open to-do list
def autoload() -> None:
	glob.todo = []
	open_file = read_open_file()
	if len(open_file):
		if open_file['type'] == "%d" and open_file['name'] != f"{glob.date}.todo":
			if f"{glob.date}.todo" in listdir(glob.LISTFILES):
				with open(path.join(glob.LISTFILES, f"{glob.date}.todo"), 'r') as f:
					glob.todo = [line.strip('\n') for line in f.readlines()]
				glob.todo.pop()
			else:
				glob.todo += open_list(open_file['name'])
				glob.todo.pop()
				rm_crossed()
				default_items()
				append_postponed()
			with open(path.join(glob.PROGFILES, "lastopen"), 'w') as f:
				f.write(f"{glob.date}.todo\n%d\n")
			return None
		try:
			with open(path.join(glob.LISTFILES, open_file['name']), 'r') as f:
				glob.todo = [line.strip('\n') for line in f.readlines()]
			glob.todo.pop()
		except FileNotFoundError or IndexError:
			clear_open_file()
			glob.todo = []
	else:
		with open(path.join(glob.PROGFILES, "lastopen"), 'w') as f:
			f.write(f"{glob.date}.todo\n%d\n")
		if file_exists(f"{glob.date}.todo"):
			glob.todo = open_list(f"{glob.date}.todo")
			glob.todo.pop()
	return None

# Implement the daily items to the to-do list
def default_items() -> None:
	rm_old_default_items()
	items = read_default_items()
	for i in range(len(items)):
		glob.todo.insert(i, items[i])
	return None

# Make sure default items don't duplicate
def rm_old_default_items() -> None:
	items = read_default_items()
	for item in items:
		if item in glob.todo:
			glob.todo.remove(item)
	return None

# Break down parenet functions ^
def read_default_items() -> list[str]:
	with open(path.join(glob.CONFFILES, "daily-default"), 'r') as f:
		items = [line.strip("\n") for line in f.readlines()]
	return items

# For moving daily items over to today's list
def rm_crossed() -> None:
	uncrossed = []
	for item in glob.todo:
		if ord(item[1]) != 822:
			uncrossed.append(item)
	glob.todo = uncrossed
	return None

# Child user-interactive function
def delete_load_file(files: list[str]) -> None:
	gnrl.slowprint('', "Enter the number corresponding to the file you would like to delete. 'c' to cancel.", '')
	while True:
		to_delete = input(" > ")
		if to_delete.isdigit():
			to_delete = int(to_delete) - 1
			if to_delete in range(len(files)):
				confirm(files[to_delete], {'type': "delete", 'pres-verb': "delete", 'past-verb': "deletion"})
				sleep(glob.SLPTM)
				return None
			else:
				gnrl.slowprint(glob.INV_FUNC)
		elif to_delete.lower() == 'c':
			gnrl.slowprint('', "Cancelled file deletion.", '')
			sleep(glob.SLPTM)
			return None
		else:
			gnrl.slowprint(glob.INV_FUNC)

# Break down parent function ^
def deleteit(filename: str) -> None:
	remove(path.join(glob.LISTFILES, filename))
	return None	

# Confirm child user-interactive function usage
def confirm(filename: str, function: dict) -> None:
	file_is_open = False
	open_file = read_open_file()
	if len(open_file) and open_file['name'] == filename:
		file_is_open = True
	if file_is_open:	
		gnrl.slowprint('', f"Are you sure you'd like to {function['pres-verb']} the file '{filename}'? This will also clear your current to-do list. (y/N)", '')
	else:
		gnrl.slowprint('', f"Are you sure you'd like to {function['pres-verb']} the file '{filename}'? (y/N)", '')
	while True:
		confirmation = input(" > ").lower()
		match confirmation:
			case 'n' | '':
				gnrl.slowprint('', f"{function['past-verb'].capitalize()} of file '{filename}' cancelled.", '')
				return None
			case 'y':
				if file_is_open:
					clear_open_file()
					glob.todo = []	
				if function['type'] == "delete":
					deleteit(filename)
					gnrl.slowprint('', "File successfully deleted.", '')
				elif function['type'] == "archive":
					archiveit(filename)
					archived_path = path.join(glob.LISTFILES, "archive", filename)
					gnrl.slowprint('', f"File successfully archived. It can be found at '{archived_path}'.", '')
				return None
			case _:
				gnrl.slowprint(glob.Y_OR_N)

# Append the postponed file in PROGFILES
def append_postponed() -> None:
	with open(path.join(glob.PROGFILES, "postpone"), 'r') as f:
		glob.todo += [line.strip('\n') for line in f.readlines()]
	with open(path.join(glob.PROGFILES, "postpone"), 'w'):
		pass
	return None

# Read the current open file name and type
def read_open_file() -> dict[str, str]:
	with open(path.join(glob.PROGFILES, "lastopen"), 'r') as f:
		open_file = [line.strip('\n') for line in f.readlines()]
	if len(open_file):
		return {'name': open_file[0], 'type': open_file[1]}
	return {}

# Clear the current open file name and type
def clear_open_file() -> None:
	with open(path.join(glob.PROGFILES, "lastopen"), 'w'):
		return None
