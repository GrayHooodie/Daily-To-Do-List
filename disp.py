from time import sleep
from os import system, path, makedirs, listdir, getlogin, rename, remove

import dtdl, glob, fman, lman

def list_items(todo: list[str]) -> None:
	open_file = fman.read_open_file()
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

def list_files(*function_header: str) -> None:
	open_file = fman.read_open_file()
	if len(open_file):
		disp_open_file = f"\nCurrent File: {open_file["name"]}"
	else:
		disp_open_file = ''
	slowprint(function_header[0], function_header[1], f"{disp_open_file}", '', "Files:", '')
	files = fman.get_file_names()
	num = 1
	for file in files:
		if num < 10:
			slowprint(f" {num}.  {file}")
		else:
			slowprint(f" {num}. {file}")
		num += 1
	slowprint('')	
	return None

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

def edit_items_menu(todo: list[str]) -> None:
	system("clear")
	slowprint("[editing items]", "---------------", '')
	list_items(todo)
	return None

def postpone_items_menu(todo: list[str]) -> None:
	system("clear")
	slowprint("[postponing items]", "------------------", '')
	list_items(todo)
	return None

def rm_items_menu(todo: list[str]) -> None:
	system("clear")
	slowprint("[removing items]", "----------------", '')
	list_items(todo)
	return None

def save_menu():
	system("clear")
	open_file = fman.read_open_file()
	list_files("[saving file]", "-------------")
	files = fman.get_file_names()
	if len(openfile) and fman.file_exists(open_file["name"]):
		slowprint('', f"Name your file, or empty return to overwrite '{open_file["name"]}'. 'c' to cancel.", '')
	elif f"{date}.todo" not in files:
		slowprint('', f"Name your file, or empty return to name the file '{date}'. 'c' to cancel.", '')
	else:
		slowprint('', "Name your file, or enter the corresponding number to overwrite a file. 'c' to cancel.", '')
	return None

def load_menu() -> None:
	system("clear")
	list_files("[loading file]", "--------------")
	slowprint('', "Enter the number of file you would like to open. 'r' to rename a file. 'd' to delete a file. 'a' to archive a file. 'c' to cancel.", '')
	return None

def title() -> None:
	system("clear")
	slowprint('', "---------------------------", "Welcome to your to-do list!", "---------------------------", '')
	return None

def slowprint(*text) -> None:
	delay: float = 0.02
	for line in text:
		print(line)
		sleep(delay)
	return None

def menu(todo: list[str], justopened: bool) -> None:
	system("clear")
	if justopened:
		title()
	list_items(todo)
	slowprint('', "Add an item, or cross-off an item by entering its line number. 'h' for help.", '')
	return None

def return_to_menu(todo: list[str]) -> None:
	sleep(1)
	menu(todo, False)
	return None

