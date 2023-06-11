'''
This file supports backward compatability and will be depricated
RPi automatically runs this code at start-up.
This code will check out mcp (if the folder doesn't exist), and run mcp_main.py
'''

import os
import shutil
import subprocess

if __name__ == "__main__":
    # Get the current directory of the Python script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Change path to this file's directory
    os.chdir(current_dir)
    
    # Check if mcp-flight-software folder exist
    if not os.path.isdir("mcp-flight-software"):
       # Doesn't exist, lets check out code first
        subprocess.call(["git", "clone", "https://github.com/SpaceHummus/mcp-flight-software.git","mcp-flight-software"])

    # Run main code 
    os.chdir("mcp-flight-software")
    try:
        subprocess.call(["sudo","python","main_mcp.py"])
    # Continue even if error happened
    
    # Update code using the git handler
    subprocess.call(["python","git_handler.py"])
    
    # Update self
    shutil.move("scp2_main.py", "../")
