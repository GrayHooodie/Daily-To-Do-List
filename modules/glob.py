from datetime import datetime
from os import name, path
from pathlib import Path

date: str = datetime.today().strftime('%Y-%m-%d')
if name == "nt":
    clear = "cls"
else:
    clear = "clear"

home: str = str(Path.home())
listfiles: str = path.join(home, "Documents", "To-Do Lists")
progfiles: str = path.join(home, ".dtdl", "programfiles")
ext: str = ".todo"

invalid_ln: str = "Please enter a valid line number."
invalid_fn: str = "Please enter a valid file number."
y_or_n: str = "Enter 'y' or 'n'."
no_chng: str = "No changes made."