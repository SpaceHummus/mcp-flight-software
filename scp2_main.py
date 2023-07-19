'''
This file supports backward compatability and will be depricated
RPi automatically runs this code at start-up.
This code will check out mcp (if the folder doesn't exist), and run mcp_main.py
'''

import os
import shutil
import subprocess
import sys

if __name__ == "__main__":
    # Print the options for this script
    print("Script Options:")
    print("--fresh will check out a fresh copy of the code while deleting the old copy")
    print("--loop will run main_mcp.py over and over again use ctrl+C to break"); 

    # Get the current directory of the Python script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Change path to this file's directory
    os.chdir(current_dir)
    
    # Check if "--fresh" flag was raised, if it did, user would like to delete existing folder
    if "--fresh" in sys.argv:
        subprocess.call(["sudo","rm","-rf","mcp-flight-software"])
    
    # Check if mcp-flight-software folder exist
    if not os.path.isdir("mcp-flight-software"):
       # Doesn't exist, lets check out code first
        subprocess.call(["git", "clone", "https://github.com/SpaceHummus/mcp-flight-software.git","mcp-flight-software"])

    # Run main code 
    os.chdir("mcp-flight-software")
    return_code = subprocess.call(["sudo","python","main_mcp.py"])
    while ("--loop" in sys.argv and return_code == 0):
        return_code = subprocess.call(["sudo","python","main_mcp.py"]) # Loop forever if needed
    
    # If error occured, try updating
    if return_code != 0:
        print("Preforming git update to try and resolve this issue")
        subprocess.call(["git", "pull", "--force"])
    
    # Update self
    if os.path.exists("scp2_main.py"):
        print("Preforming self update")
        dest_path = "../scp2_main.py"
        if os.path.exists(dest_path):
            os.remove(dest_path)
        shutil.move("scp2_main.py", "../")
