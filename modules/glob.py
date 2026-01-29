from datetime import datetime
from os import name, path
from pathlib import Path


def get_tweak_value(tweakname: str, default: int or float):
    with open(usr_tweaks, 'r') as f:
        tweak = [line.strip('\n') for line in f.readlines() if tweakname in line]
        print(tweak)
    if len(tweak) and len(tweak[0].split('=')) == 2:
        return tweak[0].split('=')[1]
    return default

def get_tweak_int(tweakname: str, default: int) -> int:
    tweak_value = get_tweak_value(tweakname, default)
    try:
        return int(tweak_value)
    except ValueError:
        return default

def get_tweak_float(tweakname: str, default: float) -> float:
    tweak_value = get_tweak_value(tweakname, default)
    try:
        return float(tweak_value)
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

invalid_ln: str = "Please enter a valid line number."
invalid_fn: str = "Please enter a valid file number."
y_or_n: str = "Enter 'y' or 'n'."
no_chng: str = "No changes made."