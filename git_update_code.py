'''
This code will update the code on the folder with this file (if there is internet connection) 
'''

import logging
import os
from setup_logging import setup_logging
import subprocess
import socket

def _check_internet_connection():
    try:
        # Check if there is internet connectivity by attempting to connect to a reliable host
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        return False
                

def _update_folder():
    # Get the current directory of the Python script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get original directory 
    original_dir = os.getcwd()
    
    # Change directory 
    os.chdir(current_dir)
    
    # Check if the MCP folder is a Git repository
    if os.path.isdir(".git"):
        logging.info("Updating from git...")
        # Use the 'git pull' command to update the repository
        #subprocess.call(["git", "pull"])
        # Do a "hard" update of the repositry, ignore all local changes
        subprocess.call(["git", "fetch", "--all"])
        subprocess.call(["git", "'reset", "--hard", "origin/master"])
        logging.info("Done")
    else:
        logging.warning("This is not a git repository")
        
    # Change directory back
    os.chdir(original_dir)
        
        
def git_update_code():
    if (_check_internet_connection()):
        logging.info("We have internet")
        _update_folder()
    else:
        logging.warning("No internet connection, skipping the update")

if __name__ == "__main__":
    setup_logging()
    git_update_code()