'''
This code will update the code on the folder with this file (if there is internet connection) 
'''

import os
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
        print("Updating folder...")
        # Use the 'git pull' command to update the repository
        subprocess.call(["git", "pull"])
    else:
        print ("This is not a git repository")
        
    # Change directory back
    os.chdir(original_dir)
        
        
def git_update_code():
    if (_check_internet_connection()):
        print("We have internet")
        _update_folder()
    else:
        print("No internet connection, skipping the update")


if __name__ == "__main__":
    git_update_code()