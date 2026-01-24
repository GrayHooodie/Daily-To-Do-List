from os import makedirs, path
from time import sleep

import modules.glob as glob

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

def enter_digit(base: int, text: dict, enter_to_confirm: bool) -> int:
	slowprint('', text["context"], '')
	while True:
		num = input(" > ")
		if num.isdigit():
			num = int(num) - base
			if num in range(len(glob.todo)):
				return num
		elif num.lower() == 'c':
			if "cancel" in text:
				slowprint('', text["cancel"], '')
			return -2
		elif enter_to_confirm and num == '':
			return -1	
		slowprint(text["line_num"])

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

def slowprint(*text) -> None:
	delay: float = 0.02
	for line in text:
		print(line)
		sleep(delay)
	return None

