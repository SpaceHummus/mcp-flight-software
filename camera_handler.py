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


# where do we store the images localy
IMAGES_DIR = "images/"

def run_camera(name):
    os.system("raspistill -t 2000")


# check if the image file name already exists, if yes, generate a new one
def fix_file_path(file_path: str) -> str:
    file = Path(file_path)
    if not file.exists():
        return str(file)
    year = 10
    name = file.name[2:]
    while year<100: # up to year 99 (2099)
        new_path = file.parent / f"{year}{name}"
        if not new_path.exists():
            return str(new_path)
        year +=1
    return str(file.parent / f"{year}{name}")

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


class CameraHandler:
    focus=512
    next_picture_index = 0

    def __init__(self,width=4056,height=3040):
        gp.setwarnings(False)
        gp.setmode(gp.BCM)

        #gp.setup(board3bcm(7), gp.OUT)
        #gp.setup(board3bcm(11), gp.OUT)
        #gp.setup(board3bcm(12), gp.OUT)

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
    def change_focus(self,focus):
        self.focus = focus
        logging.info("changing focus to:%d",focus)
        x = threading.Thread(target=run_camera, args=(1,))
        x.start()
        time.sleep(2)
        arducam_vcm.vcm_write(focus)
        time.sleep(3)
        
    # Take a picture, at current focus. Return file path to the picture.
    # File format is <Picture #>_<Focus>_<file_suffix>.jpg
    def take_pic (self, 
        folder_path = "./", 
        file_suffix = "", # Use file suffix to specify illumination 
        is_use_full_resolution = True, # Set to True for full resolution or False for reduced resolution, but easier to send data
        ):
        
        # Generate filepath
        new_file_name="{0}{0:04d}_F{1:04d}_{2}.jpg".format(
            folder_path,
            self._take_pic_increment_index_by_one()
            self.focus,
            "_" + file_suffix if file_suffix else ""
            )
        new_file_name = Path(new_file_name)
        
        # Generate command string according to is_use_full_resolution
        # Use -vf -hf flags to flip the image vertically or horizontically if needed
        if is_use_full_resolution:
            cmd = "raspistill -o %s" %new_file_name
        else:
            cmd = "raspistill -w 640 -h 480 -n -t 100 -q 20 -e jpg -th none -o %s" %file_name
        
        # Take the picture
        logging.info("taking picture, file path: %s",file_name)
        logging.debug("Command: %s",cmd)
        print(cmd)
        os.system(cmd)
        logging.info("Done taking picture")
        
        return new_file_name
        
    # This is an auxilary function to get next image index from file, and increase that number by 1
    def _take_pic_increment_index_by_one(self):
        try:
            # Try to open the file for reading
            with open(filename, 'r') as file:
                # Read the current number from the file
                n = int(file.read().strip())
                
        except Exception as e:
            logging.warning(f"Can't determine n: {e}")
            # Handle file not found or corrupted (invalid content)
            n = 0
        
        # Increment the number and write it back to the file
        try:
            with open(filename, 'w') as file:
                file.write(str(n + 1))
        except Exception as e:
            logging.warning(f"Error writing to file: {e}")

        # Return the original number (before incrementing)
        return n




if __name__ == "__main__":
    camera = CameraHandler()
    camera.change_focus(100)
    camera.take_pic(is_use_full_resolution=True)
    camera.change_focus(900)
    camera.take_pic(is_use_full_resolution=False)