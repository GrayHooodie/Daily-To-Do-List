from os import getlogin, listdir, makedirs, path, remove, rename, system
from time import sleep

import modules.fman as fman
import modules.glob as glob
import modules.gnrl as gnrl
import modules.twks as twks


def list_items() -> None:
	start_splice = (twks.page - 1) * twks.pagelength
	if start_splice + twks.pagelength <= len(glob.todo):
		end_splice = start_splice + twks.pagelength
	else:
		end_splice = len(glob.todo)
	open_file = fman.read_open_file()
	if len(open_file):
		gnrl.slowprint(f"Current File: {open_file["name"]}")
	gnrl.slowprint('', "To-Do List:", '')
	if len(glob.todo):
		num = 1
		for _ in range(twks.page - 1):
			num += twks.pagelength
		for item in glob.todo[start_splice:end_splice]:
			if num < 10:
				gnrl.slowprint(f" {num}.   {item}")
			elif num < 100:
				gnrl.slowprint(f" {num}.  {item}")
			else:
				gnrl.slowprint(f" {num}. {item}")
			num += 1
		if twks.page > 1:
			last_page = str(twks.page - 1) 
		else:
			last_page = ' '
		cur_page = str(twks.page) + '\u0332'
		if twks.page < twks.pages:
			next_page = str(twks.page + 1)
		else:
			next_page = ' '
		gnrl.slowprint('', f"p: {last_page} {cur_page} {next_page}", '')
	else:
		gnrl.slowprint(" (Empty)")
	gnrl.slowprint('')
	return None

def list_files(*function_header: str) -> None:
	open_file = fman.read_open_file()
	files = fman.get_file_names()
	gnrl.slowprint(function_header[0], function_header[1])
	if len(open_file):
		gnrl.slowprint(f"\nCurrent File: {open_file["name"]}")
	if len(files):
		gnrl.slowprint('', "Files:", '')
	num = 1
	for file in files:
		if num < 10:
			gnrl.slowprint(f" {num}.  {file}")
		else:
			gnrl.slowprint(f" {num}. {file}")
		num += 1
	gnrl.slowprint('')	
	return None

def confirm_edits_text(is_equal: bool, function: str) -> None:
	if is_equal:
		gnrl.slowprint('', glob.no_chng, '')
	else:
		gnrl.slowprint('', f"Item(s) successfully {function}.", '')
	return None

def arrange_items_menu() -> None:
	system(glob.clear)
	gnrl.slowprint("[arranging items]", "-----------------", '')
	list_items()
	return None

def edit_items_menu() -> None:
	system(glob.clear)
	gnrl.slowprint("[editing items]", "---------------", '')
	list_items()
	return None

def postpone_items_menu() -> None:
	system(glob.clear)
	gnrl.slowprint("[postponing items]", "------------------", '')
	list_items()
	return None

def rm_items_menu() -> None:
	system(glob.clear)
	gnrl.slowprint("[removing items]", "----------------", '')
	list_items()
	return None

def save_menu():
	system(glob.clear)
	open_file = fman.read_open_file()
	list_files("[saving file]", "-------------")
	files = fman.get_file_names()
	if len(open_file) and fman.file_exists(open_file["name"]):
		gnrl.slowprint('', f"Name your file, or empty return to overwrite '{open_file["name"]}'. 'c' to cancel.", '')
	elif f"{glob.date}.todo" not in files:
		gnrl.slowprint('', f"Name your file, or empty return to name the file '{glob.date}'. 'c' to cancel.", '')
	else:
		gnrl.slowprint('', "Name your file, or enter the corresponding number to overwrite a file. 'c' to cancel.", '')
	return None

def load_menu() -> None:
	system(glob.clear)
	list_files("[loading file]", "--------------")
	gnrl.slowprint('', "Enter the number of file you would like to open. 'r' to rename a file. 'd' to delete a file. 'a' to archive a file. 'c' to cancel.", '')
	return None

def title() -> None:
	gnrl.slowprint('', "---------------------------", "Welcome to your to-do list!", "---------------------------", '')
	return None

def menu(justopened: bool, bypass: bool) -> None:
	if bypass:
		return None
	system(glob.clear)
	if justopened:
		title()
	list_items()
	gnrl.slowprint('', "Add an item, or cross-off an item by entering its line number. 'h' for help.", '')
	return None