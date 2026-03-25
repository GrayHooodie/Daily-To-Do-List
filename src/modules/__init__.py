from subprocess import call 
import sys 

# CHANGE EACH UPDATE 
RELEASE_NUM = "v1.1.5" 

# Handles command line flags 
if len(sys.argv) > 1: 
    if len(sys.argv) > 2: 
        print("\ndtdl can only take one flag for input ('-v', '--version', 'h', '--help').\n") 
    elif sys.argv[1] in ["-v", "--version", "-h", "--help"]: 
        if 'v' in sys.argv[1]: 
            print(f"\ndtdl --- {RELEASE_NUM}\n") 
        elif 'h' in sys.argv[1]: 
            print("\n'-h', '--help'       ---    Show this help screen") 
            print("'-v', '--version'    ---    Show the current installed version of the program\n") 
        sys.exit(0) 
    else: 
        print(f"\nUnknown flag '{sys.argv[1]}'. You may use one of the following flags: '-v', '--version', '-h', '--help'\n") 
    sys.exit(1) 

# Local modules imports 
import modules.setup as setup 
import modules.disp as disp 
import modules.fman as fman 
import modules.glob as glob 
import modules.gnrl as gnrl 
import modules.progfuncs as pf 
import modules.twks as twks 
