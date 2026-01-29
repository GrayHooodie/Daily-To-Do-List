from datetime import datetime
from os import name, path
from pathlib import Path


def get_tweak_value(tweakname: str, default: int or float) -> int:
    for line in tweaks:
        if tweakname in line:
            if len(line.split('=')) == 2:
                return line.split('=')[1]
    return default

def get_tweak_int(tweakname: str, default: int) -> int:
    try:
        return int(get_tweak_value(tweakname, default))
    except ValueError:
        return default

def get_tweak_float(tweakname: str, default: float) -> float:
    try:
        return float(get_tweak_value(tweakname, default))
    except ValueError:
        return default


if name == "nt":
    clear = "cls"
else:
    clear = "clear"

todo: list[str] = []
date: str = datetime.today().strftime('%Y-%m-%d')
home: str = str(Path.home())
listfiles: str = path.join(home, "Documents", "To-Do Lists")
conffiles: str = path.join(home, ".dtdl", "config")
progfiles: str = path.join(home, ".dtdl", "programfiles")
def_tweaks: str = path.abspath(path.join(path.dirname(__file__), "..", "defaults", "tweaks.conf"))
usr_tweaks: str = path.join(conffiles, "tweaks.conf")
ext: str = ".todo"
slptm = 1.5

# app tweaks (user can set these)
with open(usr_tweaks, 'r') as f:
    tweaks = [line.split('\n') for line in f.readlines()]

# maxlength
maxlength = get_tweak_int("maxvalue", 50)

# printspeed
textspeed = get_tweak_float("textspeed", 0.02)

invalid_ln: str = "Please enter a valid line number."
invalid_fn: str = "Please enter a valid file number."
y_or_n: str = "Enter 'y' or 'n'."
no_chng: str = "No changes made."