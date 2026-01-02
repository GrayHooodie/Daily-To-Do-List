from datetime import datetime
from os import getlogin

usr: str = getlogin()
date: str = datetime.today().strftime('%Y-%m-%d')

listfiles: str = f"/home/{usr}/Documents/To-Do Lists"
progfiles: str = f"/home/{usr}/.todolist/programfiles"
ext: str = ".todo"

invalid_ln: str = "Please enter a valid line number."
invalid_fn: str = "Please enter a valid file number."
y_or_n: str = "Enter 'y' or 'n'."
no_chng: str = "No changes made."