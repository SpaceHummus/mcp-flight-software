'''
This code will update the code on the folder with this file (if there is internet connection) 
'''

import logging
import os
from setup_logging import setup_logging
import subprocess
import socket

class GitHandler:

##################### Change folders to/from git folder #####################
    original_dir = None
    def _change_to_git_folder(self):
        # Get the current directory of the Python script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Get original directory 
        self.original_dir = os.getcwd()
        
        # Change directory 
        os.chdir(current_dir)
    
    def _change_folder_back(self):
        os.chdir(self.original_dir)

##################### End of change folders to/from git folder #####################                    

    def _check_internet_connection(self):
        try:
            # Check if there is internet connectivity by attempting to connect to a reliable host
            socket.create_connection(("www.google.com", 80))
            return True
        except OSError:
            return False

    def _update_folder(self):
        
        self._change_to_git_folder()
        
        # Check if the MCP folder is a Git repository
        if os.path.isdir(".git"):
            logging.info("Updating from git...")
            # Use the 'git pull' command to update the repository, ignore all local changes
            subprocess.call(["git", "pull", "--force"])
            logging.info("Done")
        else:
            logging.warning("This is not a git repository")
            
        self._change_folder_back()
            
    def git_update_code(self):
        if (_check_internet_connection()):
            logging.info("We have internet")
            self._update_folder()
        else:
            logging.warning("No internet connection, skipping the update")
            
    def git_get_version(self):
        # Execute git command to retrieve version information
        self._change_to_git_folder()
        result = subprocess.check_output(['git', 'describe', '--tags'], stderr=subprocess.STDOUT)
        self._change_folder_back()
        
        version = result.decode().strip()        
        logging.info("Current repository version " + version)
        return version

if __name__ == "__main__":
    setup_logging()
    g = GitHandler()
    g.git_get_version()
    g.git_update_code()
    g.git_get_version()