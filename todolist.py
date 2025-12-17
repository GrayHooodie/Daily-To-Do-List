# Simple todo-list program made by Matt L on 2025/12/11 while not wanting to go to sleep

from datetime import datetime
from time import sleep
from os import system, path, makedirs, listdir, getlogin, rename, remove



usr = getlogin()
date = datetime.today().strftime('%Y-%m-%d')
listfiles = f"/home/{usr}/Documents/To-do Lists"
progfiles = f"/home/{usr}/.todolist/programfiles"
# ==================== functions =====================

def list_items(list):
	title = ("", "To-Do List:", "")
	bottom = ("", "")
	slowprint(title)
	if len(list) > 0:
		num = 1
		for item in list:
			if num < 10:
				slowprint(f" {num}.  {item}")
			else:
				slowprint(f" {num}. {item}")
			num += 1
	else:
		slowprint(" (Empty)")
	slowprint(bottom)
	return

def sort_items(list):
	uncrossed = []
	crossed = []
	for item in list:
		if ord(item[1]) == 822:
			crossed.append(item)
		else:
			uncrossed.append(item)
	return uncrossed + crossed

def cross(list, line):
	if line in range(1, len(list) + 1):
		if ord(list[line - 1][1]) == 822:
			list[line - 1] = unstrike(list[line - 1])
		else:
			list[line - 1] = strike(list[line - 1])
	else:
		slowprint(("", "Please enter a valid line number to cross-off.", ""))
	return list

# arrange items menu title
def arrange_items_menu(list):
	system("clear")
	slowprint(("[arranging items]", "-----------------", ""))
	list_items(list)
	slowprint(("Enter the line number you would like to move. Empty return to finish arranging items. 'c' to cancel.", ""))
	return

# move lines around to user's liking
def arrange_items(list):

	# option to cancel the changes
	unchanged = list.copy()

	# display the menu text
	arrange_items_menu(list)

	while True:
		line = input(" > ")
		# to check for different input types
		if line.isdigit():
			line = int(line)
			if line in range(1, len(list) + 1):
				# where shall this line move to?
				slowprint(("", f"Enter the new position of line {line}. Empty return to cancel line {line} arrangement.", ""))
				while True:
					dest = input(" > ")
					# if a number is inputted
					if dest.isdigit():
						# cast to an int
						dest = int(dest)
						# if it's a selection of an available line number
						if dest in range(1, len(list) + 1):
							# make copy of list item
							item = list[line - 1]
							# remove item from list
							list.remove(item)
							# insert at correct destination
							list.insert(dest - 1, item)
							# redisplay the menu text
							arrange_items_menu(list)
							# break out of nested while loop
							break
						# inputted int was not an available line number
						else:
							slowprint(("", "Please enter a valid line number.", ""))
					# input was an empty return
					elif dest == "":
						# cancel the current line arrangement, break out of nested while loop
						slowprint(("", f"Cancelled arrangement of line {line}", ""))
						sleep(1)
						arrange_items_menu(list)
						break
					# input was not a line number
					else:
						slowprint(("", "Please enter a valid line number.", ""))
			# inputted int was not an available line number
			else:
				slowprint(("", "Please enter a valid line number.", ""))
		# cancel all arrangement changes
		elif line == "c":
			slowprint(("", "No changes made.", ""))
			# returns the unmodified list
			return unchanged
		# input was an empty return, saving changes if any
		elif line == "":
			if list == unchanged:
				slowprint(("", "No changes made.", ""))
			else:
				slowprint(("", "Items successfully arranged.", ""))
			return list
		# input was not a line number
		else:
			slowprint(("", "Please enter a valid line number.", ""))

def edit_items_menu(list):
	system("clear")
	slowprint(("[editing items]", "---------------", ""))
	list_items(list)
	slowprint(("Enter the line number you would like to edit. Empty return to finish editing items. 'c' to cancel.", ""))
	return

def edit_items(list):

	unchanged = list.copy()

	edit_items_menu(list)
	while True:
		line = input(" > ")
		if line.isdigit():
			line = int(line)
			if line in range(1, len(list) + 1):
				slowprint(("", f"Enter the new text for line {line}. Empty return to cancel edits on line {line}.", ""))
				while True:
					edited = input(" > ")
					if len(edited) > 1:
						if edited.isdigit():
							slowprint(("", f"Item can't be a number.", ""))
						else:
							list.remove(list[line - 1])
							list.insert(line - 1, edited)
							edit_items_menu(list)
							break
					elif edited == "":
						slowprint(("", f"Cancelled edits on line {line}", "", "Enter the line number you would like to edit. Empty return to finish editing items. 'c' to cancel.", ""))
						break
					else:
						slowprint(("", "Item must be longer than one character.", ""))
			else:
				slowprint(("", "Please enter a valid line number.", ""))
		elif line == "c":
			slowprint(("", "No changes made.", ""))
			return unchanged
		elif line == "":
			if list == unchanged:
				slowprint(("", "No changes made.", ""))
			else:
				slowprint(("", "Items successfully edited.", ""))
			return list
		else:
			slowprint(("", "Please enter a valid line number.", ""))

def rm_items_menu(list):
	system("clear")
	slowprint(("[removing items]", "----------------", ""))
	list_items(list)
	slowprint(("Enter line number(s) to remove. Empty return to finish removing items. 'c' to cancel.", ""))
	return

def rm_items(list):
	rm_items_menu(list)
	unchanged = list.copy()
	while True:
		line = input(" > ")
		if line.isdigit():
			line = int(line)
			if line in range(1, len(list) + 1):
				list.pop(line - 1)
				rm_items_menu(list)
			else:
				slowprint(("", "Please enter a valid line number.", ""))
		elif line == "c":
			slowprint(("", "No changes made.", ""))
			return unchanged
		elif line == "":
			if list == unchanged:
				slowprint(("", "No changes made.", ""))
			else:
				slowprint(("", "Line(s) deleted.", ""))
			return list
		else:
			slowprint(("", "Please enter a valid line number.", ""))

def clear(list):
	slowprint(('', "Are you sure you want to clear your to-do list? (y/N)", ''))
	while True:
		check = input(" > ")
		match check:
			case 'y' | 'Y':
				with open(f"{progfiles}/lastopen", 'w') as f:
					pass
				slowprint(('', "To-do list cleared.", ''))
				return []
			case 'n' | 'N' | '':
				slowprint(('', "Nothing changed.", ''))
				return list 
			case _:
				slowprint("Enter 'y' or 'n'.")

def prompt_save(list):
	slowprint(('', "Would you like to save your to-do list? (Y/n)", ''))
	while True:
		will_save = input(" > ")
		match will_save:
			case 'n' | 'N':
				return
			case 'y' | 'Y' | '':
				save(list)
				sleep(1)
				return
			case _:
				slowprint("Enter 'y' or 'n'.")

def save_menu():
	system("clear")
	slowprint(("[saving file]", "-------------", '', '', "Files:", ''))
	files = listdir(listfiles)
	num = 1
	for file in files:
		if num < 10:
			slowprint(f" {num}.  {file}")
		else:
			slowprint(f" {num}. {file}")
		num += 1

	if f"{date}.todo" in files:
		slowprint(('', '', f"Name your file, or enter the corresponding number to overwrite it. 'c' to cancel.", ''))
	else:
		slowprint(('', '', f"Name your file, or enter the corresponding number to overwrite it. Empty return to name the file '{date}.todo'. 'c' to cancel.", ''))
	return files

def save(list):
	files = save_menu()
	while True:
		file = input(" > ")
		if file.isdigit():
			file = int(file) - 1
			if file in range(len(files)):
				if overwrite_save(files[file]):
					file = files[file].split(".todo")[0]
					break
			else:
				slowprint("Enter a valid file number, or name your file.")
		elif file == '':
			if f"{date}.todo" in files:
				slowprint("Please name your file.")
			else:
				file = date
				break
		elif file == 'c':
			slowprint(('', "Cancelled save file.", ''))
			sleep(1)
			return
		elif f"{file}.todo" in files:
			if overwrite_save(file):
				break
		else:
			break
	with open(f"{progfiles}/lastopen", 'w') as f:
		f.write(f"{file}.todo")
		if file == date:
			f.write("\n%d")
		else:
			f.write("\n%c")
	with open(f"{listfiles}/{file}.todo", 'w') as f:
		for items in list:
			f.write("%s\n" %items)
		if file == date:
			f.write("%d")
		else:
			f.write("%c")
	slowprint(('', f"File written successfully to '{listfiles}/{file}.todo'.", ''))
	return

def overwrite_save(file):
	slowprint(('', f"'{file}.todo' already exists. Would you like to overwrite it? (y/N)", ''))
	while True:
		will_overwrite = input(" > ")
		match will_overwrite:
			case 'n' | 'N' | '':
				save_menu()
				return False
			case 'y' | 'Y':
				return True
			case _:
				slowprint("Enter 'y' or 'n'.")

def autosave(list):
	with open(f'{progfiles}/lastopen', 'r') as f:
		file = [line.strip('\n') for line in f.readlines()]
	if len(file):
		with open(f'{listfiles}/{file[0]}', 'w+') as f:
			for items in list:
				f.write('%s\n' %items)
			f.write(f'{file[1]}')
		slowprint(('', f"Saved list to '{file[0]}'.", ''))
		sleep(1)
	else:
		prompt_save(list)
	return

def load_menu():
	system("clear")
	slowprint(("[loading file]", "--------------", '', '', "Files:", ''))
	files = listdir(listfiles)
	num = 1
	for file in files:
		if num < 10:
			slowprint(f" {num}.  {file}")
		else:
			slowprint(f" {num}. {file}")
		num += 1
	slowprint(('', '', "Enter the number of file you would like to open. 'r' to rename a file. 'd' to delete a file. Empty return to cancel.", ''))
	return files

def load(unchanged):
	if not len(listdir(listfiles)):
		slowprint(('', "No files to show.", ''))
		return unchanged
	files = load_menu()
	list = []
	while True:
		select = input(" > ")
		if select.isdigit():
			select = int(select)
			if select in range(1, len(files) + 1):
				with open(f"{listfiles}/{files[select - 1]}", 'r') as f:
					for line in f.readlines():
						list.append(line.strip('\n'))
				with open(f'{progfiles}/lastopen', 'w') as f:
					f.writelines([f'{files[select - 1]}', f'\n{list[-1]}'])
				list.pop()
				break
			else:
				slowprint("Enter a valid file number.")
		elif select == '':
			slowprint(('', "No file loaded.", ''))
			return unchanged
		elif select == 'r' or select == 'R':
			rename_load_file(files)
			files = load_menu()
		elif select == 'd' or select == 'D':
			delete_load_file(files)
			files = load_menu()
		else:
			slowprint("Enter a valid file number.")
	slowprint(('', f"File {files[select - 1]} successfully loaded.", ''))
	return list

def rename_load_file(files):
	slowprint(('', "Enter the number corresponding to the file you would like to rename. Empty return to cancel.", ''))
	while True:
		to_rename = input(" > ")
		if to_rename.isdigit():
			to_rename = int(to_rename) - 1
			if to_rename in range(len(files)):
				slowprint(('', f"Enter the new name of '{files[to_rename].split(".todo")[0]}'. Empty return to cancel.", ''))
				while True:
					new_name = input(" > ")
					if new_name == '':
						slowprint(('', f"Cancelled renaming of '{files[to_rename].split(".todo")[0]}'.", ''))
						sleep(1)
						return
					if not new_name in files:
						with open(f"{progfiles}/lastopen", 'r') as f:
							open_file = [line.strip('\n') for line in f.readlines()]
						if len(open_file) and files[to_rename] == open_file[0]:
							open_file[0] = f"{new_name}.todo"
							with open(f"{progfiles}/lastopen", 'w') as f:
								f.writelines([f'{open_file[0]}', f'\n{open_file[1]}'])
						rename(f"{listfiles}/{files[to_rename]}", f"{listfiles}/{new_name}.todo")
						return
					else:
						slowprint(f"Name '{new_name}' already in use. Try again.")
			else:
				slowprint(f"'{to_rename}' is not a valid file number.")
		elif to_rename == '':
			slowprint(('', "Cancelled renaming.", ''))
			sleep(1)
			return 
		else:
			slowprint("Please enter a valid file number.")

def delete_load_file(files):
	slowprint(('', "Enter the number corresponding to the file you would like to delete. Empty return to cancel.", ''))
	while True:
		to_delete = input(" > ")
		if to_delete.isdigit():
			to_delete = int(to_delete) - 1
			if to_delete in range(len(files)):
				slowprint(('', f"Are you sure you'd like to delete the file '{files[to_delete]}'? (y/N)", ''))
				while True:
					confirm_delete = input(" > ")
					match confirm_delete:
						case 'n' | 'N' | '':
							slowprint(('', f"Deletion of file '{files[to_delete]}' cancelled.", ''))
							sleep(1)
							return 
						case 'y' | 'Y':
							with open(f"{progfiles}/lastopen", 'r') as f:
								open_file = [line.strip('\n') for line in f.readlines()]
							if len(open_file) and open_file[0] == files[to_delete]:
								with open(f"{progfiles}/lastopen", 'w') as f:
									pass
							remove(f"{listfiles}/{files[to_delete]}")
							return 
						case _:
							slowprint("Enter 'y' or 'n'.")
			else:
				slowprint("Please enter a valid file number.")
		elif to_delete == '':
			slowprint(('', "Cancelled file deletion.", ''))
			sleep(1)
			return 
		else:
			slowprint("Please enter a valid line number.")
							
def autoload():
	list = []

	with open(f'{progfiles}/lastopen', 'r') as f:
		file = [line.strip('\n') for line in f.readlines()]
	if len(file):
		if file[1] == '%d' and file[0] != f'{date}.todo':
			with open(f'{progfiles}/lastopen', 'w') as f:
				f.writelines([f'{date}.todo', '\n%d'])
			return list
		try:
			with open(f'{listfiles}/{file[0]}', 'r') as f:
				for line in f.readlines():
					list.append(line.strip('\n'))
				list.pop()
		except:
			pass
	elif f"{date}.todo" not in listdir(listfiles):
		with open(f"{progfiles}/lastopen", 'w') as f:
			f.writelines([f"{date}.todo", "\n%d"])
	return list

def file_integrity():
	if not path.exists(f'{progfiles}/'):
		makedirs(f'{progfiles}/')
	if not listdir(f'{progfiles}'):
		with open(f'{progfiles}/lastopen', 'w+') as f: 
			f.writelines([f'{date}.todo', '\n%d'])
	if not path.exists(f'{listfiles}/'):
		makedirs(f'{listfiles}/')
	return

def title():
	system("clear")
	slowprint(('', "---------------------------", "Welcome to your to-do list!", "---------------------------", ''))
	return

# for getting the strikethrough on strings
def strike(text):
	new_text = ''
	for c in text:
		new_text += c + "\u0336"
	return new_text

def unstrike(text):
	new_text = ''
	for i in range(0, len(text), 2):
		new_text += text[i]
	return new_text

def slowprint(text):
	delay = 0.02
	if type(text) == tuple:
		for line in text:
			print(line)
			sleep(delay)
	elif type(text) == str:
		print(text)
		sleep(delay)
	return

# display edit menu title
def menu(list, justopened):
	system("clear")
	if justopened:
		title()
	list_items(list)
	slowprint(("Add items, or cross-off items by entering their line number(s). 'h' for help.", ""))
	return

# returning to the edit menu from another function
def return_to_menu(list):
	sleep(1)
	menu(list, False)
	return


# ======================== functions ===========================

def main():
	file_integrity()
	# help menu in a list so i can slowprint it
	help = ("", "'s'  Sort Items", "'a'  Arrange Items", "'e'  Edit Items", "'r'  Remove Items", "", "'C'  Clear List", "'S'  Save List To File", "'L'  Load List From File", "", "'h'  Show This Help Text", "'q'  Quit", "")

	list = autoload()
	menu(list, True)
	while True:
		item = input(" > ")

		if item.isdigit():
			item = int(item)
			if item in range(0, len(list) + 1):
				cross(list, item)		
				menu(list, False)
			else:
				slowprint(("", "Please enter a valid line number to cross-off.", ""))
		
		else:
			# maybe change this so letters' capital and lower can do different things
			match item:

				# list the items in todo list
				case "":
					menu(list, False)
				case "s":
					list = sort_items(list)
					menu(list, False)
				# open arrange menu
				case "a" | "A":
					if len(list) > 1:
						list = arrange_items(list)
						return_to_menu(list)
					else:
						slowprint(("", "Must have at least 2 list items to arrange.", ""))
				# open edit menu
				case "e" | "E":
					if len(list) > 0:
						list = edit_items(list)
						return_to_menu(list)
					else:
						slowprint(("", "Must have at least 1 list item to edit.", ""))
				# open remove items menu
				case "r" | "R":
					if len(list) > 0:
						list = rm_items(list)
						return_to_menu(list)
					else:
						slowprint(("", "Must have at least 1 list item to remove.", ""))
				# prompt to confirm list deletion
				case "c" | "C":
					list = clear(list)
					return_to_menu(list)
				case "S":
					if len(list) > 0:
						save(list)
						return_to_menu(list)
					else:
						slowprint(("", "Must have a list to save.", ""))
				case "L":
					list = load(list)
					return_to_menu(list)
				# help text
				case "h" | "H":
					slowprint(help)
				case "q" | "Q":
					if len(list):
						autosave(list)
					system("clear")
					return 0
				# add item to list if it's more than one char
				case _:
					if len(item) > 1:
						list.append(item)
						menu(list, False)
					else:
						slowprint(f"Unknown command '{item}'.") 

if __name__ == '__main__':
	main()
