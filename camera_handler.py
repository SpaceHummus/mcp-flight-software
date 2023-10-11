from ast import Return
import logging
import RPi.GPIO as gp
import os
from ctypes import *
arducam_vcm =CDLL('./libarducam_vcm.so')
import time
from datetime import datetime
import threading
from pathlib import Path
from setup_logging import setup_logging
import led_mode_report

# Determine folder in which this file is present
CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))

def run_camera(name):
    os.system("raspistill -t 2000")

# convert board pin numbering to bcm numbering
def board3bcm(pin):
    if pin==7:
        return 4
    elif pin == 11:
        return 17
    elif pin == 12:
        return 18
    elif pin == 15:
        return 22
    elif pin == 16:
        return 23
    elif pin == 21:
        return 9
    elif pin == 22:
        return 25
       
# Return how many pictures taken so far       
def how_many_pictures_taken():
    # Get next number from file
    try:
        # Try to open the file for reading
        file_path = Path(CURRENT_FOLDER + "/" + "pic_number.txt")
        with open(file_path, 'r') as file:
            # Read the current number from the file
            n = int(file.read().strip())
            
    except Exception as e:
        logging.warning(f"Can't determine n:\n{e}")
        # Handle file not found or corrupted (invalid content)
        n = 0
    
    return n


class CameraHandler:
    focus=512
    next_picture_index = 0

    def __init__(self,width=4056,height=3040):
        gp.setwarnings(False)
        gp.setmode(gp.BCM)
        
        gp.setup(board3bcm(11), gp.OUT)
        gp.setup(board3bcm(12), gp.OUT)

        gp.setup(board3bcm(15), gp.OUT)
        gp.setup(board3bcm(16), gp.OUT)
        gp.setup(board3bcm(21), gp.OUT)
        gp.setup(board3bcm(22), gp.OUT)
        
        gp.output(board3bcm(11), True)
        gp.output(board3bcm(12), True)

        gp.output(board3bcm(15), True)
        gp.output(board3bcm(16), True)
        gp.output(board3bcm(21), True)
        gp.output(board3bcm(22), True)

        arducam_vcm.vcm_init()

    # Change camera focus - due to a bug in the HW, we need to open a thread that starts raspstill in the backbround inparallel, why??? who knows...
    def _change_focus(self, focus):
        self.focus = focus
        logging.info("changing focus to:%d",focus)
        x = threading.Thread(target=run_camera, args=(1,))
        x.start()
        time.sleep(2)
        arducam_vcm.vcm_write(focus)
        time.sleep(3)
        
    # Take a picture, at current focus. Return file path to the picture.
    # File format is <Picture #>_<Focus>_<Mode>.jpg
    def take_pic (self, 
        focus = 512,
        folder_path = CURRENT_FOLDER, 
        is_use_full_resolution = True, # Set to True for full resolution or False for reduced resolution, but easier to send data
        ):
        
        # Change focus
        self._change_focus(focus)
        
        # Generate filepath
        mode, *_  = led_mode_report.get_led_mode_from_file()
        new_file_name="{0}/{1:04d}_F{2:04d}_{3}.jpg".format(
            folder_path,
            self._take_pic_increment_index_by_one(),
            self.focus,
            mode
            )
        new_file_name = Path(new_file_name)
        
        # Generate command string according to is_use_full_resolution
        # Use -vf -hf flags to flip the image vertically or horizontically if needed
        if is_use_full_resolution:
            cmd = "raspistill -o '%s'" %new_file_name
        else:
            cmd = "raspistill -w 640 -h 480 -n -t 100 -q 20 -e jpg -th none -o '%s'" %new_file_name
        
        # Take the picture
        logging.info("taking picture, file path: %s",new_file_name)
        logging.debug("Command: %s",cmd)
        print(cmd)
        os.system(cmd)
        logging.info("Done taking picture")
        
        return new_file_name
        
    # This is an auxilary function to get next image index from file, and increase that number by 1
    def _take_pic_increment_index_by_one(self):
        file_path = Path(CURRENT_FOLDER + "/" + "pic_number.txt")
        
        n = how_many_pictures_taken()
        
        # Increment the number and write it back to the file
        try:
            with open(file_path, 'w') as file:
                file.write(str(n + 1))
        except Exception as e:
            logging.warning(f"Error writing to file:\n{e}")

        # Return the original number (before incrementing)
        return n


if __name__ == "__main__":
    setup_logging()
    camera = CameraHandler()
    camera.take_pic(focus=100,is_use_full_resolution=True)
    camera.take_pic(focus=900, is_use_full_resolution=False)
    
    # Run calibration by trying different values
    for f in range(0, 1601, 100):
        camera.take_pic(focus=f,is_use_full_resolution=False)
