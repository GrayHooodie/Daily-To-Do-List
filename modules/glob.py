from datetime import datetime
from os import name, path
from pathlib import Path

# Make sure screen clear works on Losedows as well as Mac + Linux
if name == "nt":
    clear = "cls"
else:
    clear = "clear"

# Initialize necesary variables
show_title, bypass = True, False
todo: list[str] = []
unchanged: list[str] = []
# Get date
date: str = datetime.today().strftime('%Y-%m-%d')

# Constants
HOME: str = str(Path.home())
LISTFILES: str = path.join(HOME, "Documents", "To-Do Lists")
CONFFILES: str = path.join(HOME, ".dtdl", "config")
PROGFILES: str = path.join(HOME, ".dtdl", "programfiles")
EXT: str = ".todo"
SLPTM = 1.5

INV_LINE: str = "Please enter a valid line number."
INV_FUNC: str = "Please enter a valid file number."
Y_OR_N: str = "Enter 'y' or 'n'."
NO_CHANGE: str = "No changes made."
