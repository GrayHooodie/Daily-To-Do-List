from time import sleep

import dtdl, disp, fman, glob

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

def arrange_items(todo: list[str]) -> list[str]:
	unchanged = todo.copy()
	disp.arrange_items_menu(todo)
	first_text = ["Enter the line number you would like to move. Empty return to finish arranging items. 'c' to cancel.", invalid_ln]
	while True:
		line = enter_digit(1, len(todo), first_text, True)
		if line == -1:
			disp.confirm_edits(todo == unchanged, "arranged")
			return todo
		elif line == -2:
			disp.slowprint('', no_chng, '')
			return unchanged
		second_text = [f"Enter the new position of line {line + 1}. 'c' to cancel line {line + 1} arrangement.", invalid_ln, f"Cancelled arrangement of line {line + 1}."]
		dest = enter_digit(1, len(todo), second_text, False)
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
			disp.edit_items_menu(todo)	
			continue
		todo.remove(todo[line])
		todo.insert(line, edited)
		disp.edit_items_menu(todo)

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
		disp.postpone_items_menu(todo)
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

def rm_items(todo: list[str]) -> list[str]:
	unchanged = todo.copy()
	text = ["Enter line number(s) to remove. Empty return to finish removing items. 'c' to cancel.", invalid_ln]
	while True:
		disp.rm_items_menu(todo)
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

def load(unchanged: list[str]) -> list[str]:
	if not len(listdir(listfiles)):
		slowprint('', "No files to show.", '')
		return unchanged
	while True:
		files = get_file_names()
		disp.load_menu()
		open_file = fman.read_open_file()
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
				case 'a':
					archive_load_file(files)
				case 'd':		
					delete_load_file(files)
				case _:
					slowprint(invalid_fn)
	slowprint('', f"File {files[select]} successfully loaded.", '')
	return todo

def open_list(file: str) -> list[str]:
	if file_exists(file):	
		with open(f"{listfiles}/{file}", 'r') as f:
			return [line.strip('\n') for line in f.readlines()]

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
