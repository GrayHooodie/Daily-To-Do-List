from time import sleep
from subprocess import call

import modules.glob as glob
import modules.twks as twks

# Strike a string
def strike(text: str) -> str:
	new_text: str = ""
	for c in text:
		new_text += c + '\u0336'
	return new_text

# Unstrike a string
def unstrike(text: str) -> str:
	new_text: str = ""
	for i in range(0, len(text), 2):
		new_text += text[i]
	return new_text

# Enter a valid digit within the number of to-do list items
def enter_digit(base: int, text: dict, enter_to_confirm: bool) -> int | None:
	slowprint('', text['context'], '')
	while True:
		num = input(" > ")
		if num.isdigit():
			num = int(num) - base
			if num in range(len(glob.todo)):
				if "postpone" in text['context'] and ord(glob.todo[num][1]) == 822:
					slowprint(text['crossed'])
				else:
					return num	
			else:
				slowprint(text['line_num'])
		elif len(num) > 1 and num[0].lower() == 'p' and num[1:].isdigit():
			if int(num[1:]) in range(twks.pages + 1):
				twks.page = int(num[1:])
				return -3
			else:
				slowprint("Please enter a valid page number.")
				continue
		elif num.lower() == 'c':
			if 'cancel' in text:
				slowprint('', text['cancel'], '')
			return -2
		elif enter_to_confirm and num == '':
			return -1	
		else:
			slowprint(text['line_num'])

# Check if a string is in the same format as YYYY-MM-DD, as that's what I've chosen for this program
def is_daily(file: str) -> bool:
	isdate: list[str] = file.split('-')

	if len(isdate) == 3:
		for i in range(len(isdate)):
			if not isdate[i].isdigit():
				return False
		year, month, day = int(isdate[0]), int(isdate[1]), int(isdate[2])
		if year in range(2000, 10000) and month in range(1, 32) and day in range(1, 32):
			return True
	return False

# Print one line at a time
def slowprint(*text) -> None:
	for line in text:
		print(line)
		sleep(twks.textspeed)
	return None

# Gracefully handle ctrl+c usage
def ctrl_c_handler(f):
	def wrapper():
		while True:
			try:
				f()
				break
			except KeyboardInterrupt:
				slowprint('', '', "If you would like to exit without saving, press 'Ctrl+C' once more. Otherwise, enter anything else.", '')
				try:
					input(" > ")
					if len(glob.unchanged):
						glob.todo = glob.unchanged
					continue
				except KeyboardInterrupt:
					call(glob.clear)
					exit()
	return wrapper

