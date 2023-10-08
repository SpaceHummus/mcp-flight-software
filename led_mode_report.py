# This file records led's mode
import logging
from setup_logging import setup_logging
import os
from pathlib import Path

# Determine folder in which this file is present
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
file_path = Path(CURRENT_FOLDER + "/" + "led_mode.txt")


# Returns current led mode (mode_name,r,g,b)
def get_led_mode_from_file():
    
    try:
        # Reading from the file
        with open(file_path, 'r') as file:
            # Reading string
            mode = file.readline().strip()

            # Reading three integers
            rgb = [int(file.readline().strip()) for _ in range(3)]
            
        return (mode,rgb[0],rgb[1],rgb[2])

    except Exception as e:
        logging.warning(f"Can't determine mode:\n{e}")
        return ("Unknown",0,0,0)
    

def set_led_mode_to_file(new_mode_name, r, g, b):
    try:
        # Writing to the file with each number on a new line
        with open(file_path, 'w') as file:
            file.write(f"{new_mode_name}\n")
            file.write(f"{r}\n{g}\n{b}\n")
    except Exception as e:
        logging.warning(f"Can't save mode to file:\n{e}")
        
    

# Test functionality
if __name__ == "__main__":
    setup_logging()
    
    # Todo




