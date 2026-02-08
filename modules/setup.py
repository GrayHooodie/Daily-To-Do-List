from os import makedirs, path
from shutil import copy

import modules.glob as glob

if not path.exists(glob.progfiles):
	makedirs(glob.progfiles)
if not path.exists(glob.conffiles):
	makedirs(glob.conffiles)
if not path.exists(path.join(glob.conffiles, "daily-default")):
	with open(path.join(glob.conffiles, "daily-default"), 'w'):
		pass
if not path.exists(path.join(glob.conffiles, "tweaks.conf")):
	with open(path.join(glob.conffiles, "tweaks.conf"), 'w') as f:
		f.write("# List items to show on one page. This may be too high depending on your monitor resolution  |  Default is 50\n")
		f.write("pagelength=50\n")
		f.write("# Length of time between 2 lines of text, in seconds. I wouldn't recommend going higher than 0.05  |  Default is 0.02\n")
		f.write("textspeed=0.02\n")
if not path.exists(path.join(glob.progfiles, "lastopen")):
	with open(path.join(glob.progfiles, "lastopen"), 'w'):
		pass
if not path.exists(path.join(glob.progfiles, "postpone")):
	with open(path.join(glob.progfiles, "postpone"), 'w'):
		pass
if not path.exists(glob.listfiles):
	makedirs(glob.listfiles)
if not path.exists(path.join(glob.listfiles, "archive")):
	makedirs(path.join(glob.listfiles, "archive"))	
