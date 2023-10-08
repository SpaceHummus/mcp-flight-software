# This script read and update uptime value, this script will be called from a crontab jpb every 1 minute
# Set up crontab like so.
# In terminal 
# crontab -e
# * * * * * python3 /home/pi/mcp/mcp-flight-software/uptime_handler.py
# To save an exit: CTRL+O then hit enter twice, then CTRL+X to exit

import os
from pathlib import Path

# Determine folder in which this file is present
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
file_path = Path(CURRENT_FOLDER + "/" + "uptime.txt")

def report_min_counter():
    try:
        # Reading from the file
        with open(file_path, 'r') as file:
            time = int(f.read())
            
        return time
            
    except Exception as e:
        # No file, or file has an issue start from 0
        return 0

def increase_min_counter():
    time = report_min_counter()
    time += 1    
    
    with open(file_path, 'w') as file:
        f.write(str(time))
    
# Progress
if __name__ == "__main__":
    increase_min_counter()
