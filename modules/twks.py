from os import path

import modules.glob as glob

def get_tweak_value(tweakname: str, default: int or float):
    if path.exists(path.join(glob.conffiles, "tweaks.conf")):
        with open(path.join(glob.conffiles, "tweaks.conf"), 'r') as f:
            tweak = [line.strip('\n') for line in f.readlines() if tweakname in line]
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

page, pages, fpage, fpages = 1, 1, 1, 1
pagelength = get_tweak_int("pagelength", 50)
textspeed = get_tweak_float("textspeed", 0.02)	
