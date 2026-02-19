from os import makedirs, path

import modules.glob as glob

def file_integrity() -> None:
	# Program files
	if not path.exists(glob.PROGFILES):
		makedirs(glob.PROGFILES)
	if not path.exists(path.join(glob.PROGFILES, "lastopen")):
		with open(path.join(glob.PROGFILES, "lastopen"), 'w'):
			pass
	if not path.exists(path.join(glob.PROGFILES, "postpone")):
		with open(path.join(glob.PROGFILES, "postpone"), 'w'):
			pass
	# Configurable files
	if not path.exists(glob.CONFFILES):
		makedirs(glob.CONFFILES)
	if not path.exists(path.join(glob.CONFFILES, "daily-default")):
		with open(path.join(glob.CONFFILES, "daily-default"), 'w'):
			pass
	if not path.exists(path.join(glob.CONFFILES, "tweaks.conf")):
		with open(path.join(glob.CONFFILES, "tweaks.conf"), 'w') as f:
			f.write("# List items to show on one page. This may be too high depending on your monitor resolution  |  Default is 50\n")
			f.write("pagelength=50\n")
			f.write("# Length of time between 2 lines of text, in seconds. I wouldn't recommend going higher than 0.05  |  Default is 0.02\n")
			f.write("textspeed=0.02\n")
	# List folder
	if not path.exists(glob.LISTFILES):
		makedirs(glob.LISTFILES)
	if not path.exists(path.join(glob.LISTFILES, "archive")):
		makedirs(path.join(glob.LISTFILES, "archive"))
	return None

# Run every time program is opened
file_integrity()