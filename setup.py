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
	if path.exists(glob.def_tweaks):
		copy(glob.def_tweaks, glob.usr_tweaks)
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
