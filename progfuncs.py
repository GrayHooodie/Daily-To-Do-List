import disp, glob, gnrl, progfuncs as pf

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
		todo[line] = gnrl.unstrike(todo[line])
	else:
		todo[line] = gnrl.strike(todo[line])
	return todo

def arrange_items(todo: list[str]) -> list[str]:
	unchanged = todo.copy()
	disp.arrange_items_menu(todo)
	first_text = ["Enter the line number you would like to move. Empty return to finish arranging items. 'c' to cancel.", glob.invalid_ln]
	while True:
		line = gnrl.enter_digit(1, len(todo), first_text, True)
		if line == -1:
			disp.confirm_edits_text(todo == unchanged, "arranged")
			return todo
		elif line == -2:
			gnrl.slowprint('', glob.no_chng, '')
			return unchanged
		second_text = [f"Enter the new position of line {line + 1}. 'c' to cancel line {line + 1} arrangement.", glob.invalid_ln, f"Cancelled arrangement of line {line + 1}."]
		dest = gnrl.enter_digit(1, len(todo), second_text, False)
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
	first_text = ["Enter the line number you would like to edit. Empty return to finish editing items. 'c' to cancel.", glob.invalid_ln]
	while True:
		line = gnrl.enter_digit(1, len(todo), first_text, True)
		if line == -1:
			disp.confirm_edits_text(todo == unchanged, 'edited')
			return todo
		elif line == -2:
			gnrl.slowprint('', glob.no_chng, '')
			return unchanged
		second_text = [f"Enter the new text for line {line + 1}. 'c' to cancel edits on line {line + 1}.", "Item can't be a number.", f"Cancelled edits on line {line + 1}", "Item must be two or more characters."]
		edited = pf.edit_item_text(2, second_text)
		if edited == 'c':
			sleep(1)
			disp.edit_items_menu(todo)	
			continue
		todo.remove(todo[line])
		todo.insert(line, edited)
		disp.edit_items_menu(todo)

def edit_item_text(minlength: int, text: list[str]) -> str:
	gnrl.slowprint('', text[0], '')
	while True:
		edited = input(" > ")
		if edited.isdigit():
			gnrl.slowprint(text[1])
			continue
		elif len(edited) >= minlength:
			return edited
		elif edited.lower() == 'c':
			gnrl.slowprint('', text[2], '')
			return edited
		gnrl.slowprint(text[3])

def postpone_items(todo: list[str]) -> list[str]:
	open_file = pf.read_open_file()
	if not len(open_file):
		gnrl.slowprint("Must have a file open to postpone items.")
		return todo
	elif open_file["lstype"] == "%c":
		gnrl.slowprint("File must be a 'daily' to-do list to postpone items.")
		return todo
	unchanged = todo.copy()
	to_postpone = []
	text = ["Enter line number(s) to postpone. Empty return to finish postponing items. 'c' to cancel.", glob.invalid_ln]
	while True:
		disp.postpone_items_menu(todo)
		line = gnrl.enter_digit(1, len(todo), text, True)
		if line == -1:
			break
		elif line == -2:
			gnrl.slowprint('', glob.no_chng, '')
			return unchanged
		to_postpone.append(todo[line])	
		todo.remove(todo[line])
	pf.add_to_postpone(to_postpone)	
	disp.confirm_edits_text(todo == unchanged, "postponed")	
	return todo

def add_to_postpone(to_postpone: list[str]) -> None:
	with open(f"{glob.progfiles}/postpone", 'a') as f:
		for item in to_postpone:
			f.write(f"{item}\n")	
	return None

def append_postponed(todo: list[str]) -> list[str]:
	with open(f"{glob.progfiles}/postpone", 'r') as f:
		todo += [line.strip('\n') for line in f.readlines()]
	with open(f"{glob.progfiles}/postpone", 'w'):
		pass
	return todo

def rm_items(todo: list[str]) -> list[str]:
	unchanged = todo.copy()
	text = ["Enter line number(s) to remove. Empty return to finish removing items. 'c' to cancel.", glob.invalid_ln]
	while True:
		disp.rm_items_menu(todo)
		line = gnrl.enter_digit(1, len(todo), text, True)
		if line == -1:
			disp.confirm_edits_text(todo == unchanged, "removed")	
			if not len(todo):
				pf.clear_open_file()	
			return todo
		elif line == -2:
			gnrl.slowprint('', glob.no_chng, '')
			return unchanged
		todo.pop(line)

def clear(todo): 
	gnrl.slowprint('', "Are you sure you want to clear your to-do list? (y/N)", '')
	while True:
		check = input(" > ")
		match check:
			case 'y' | 'Y':
				pf.clear_open_file()
				gnrl.slowprint('', "To-do list cleared.", '')
				return []
			case 'n' | 'N' | '':
				gnrl.slowprint('', glob.no_chng, '')
				return todo 
			case _:
				gnrl.slowprint(glob.y_or_n)

def read_open_file() -> dict[str: str]:
	with open(f"{glob.progfiles}/lastopen", 'r') as f:
		open_file = [line.strip('\n') for line in f.readlines()]
	if len(open_file):
		return {"name": open_file[0], "lstype": open_file[1]}
	return {}

def clear_open_file() -> None:
	with open(f"{glob.progfiles}/lastopen", 'w'):
		return None