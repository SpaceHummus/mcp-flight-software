'''
This is the main function to be executed by linux computer.
It runs as a "single shot". Collects telemetry, decides what is the next thing to do, then dies.
'''
from git_handler import GitHandler
import logging
from telemetry_handler import TelemetryHandler
from setup_logging import setup_logging
from led_service import set_led_mode
from camera_handler import CameraHandler
import camera_preprocess
import time
import zipfile
import os

# Camera parameters
NEAR_FOCUS=600
FAR_FOCUS=1000
IS_USE_FULL_RESOLUTION=True
IS_IN_SPACE=False

if __name__ == "__main__":
    setup_logging()
    
    # Start a new csv file
    if os.path.exists('telemetry.csv'):
        os.remove('telemetry.csv')

    # Define the services that would be used
    logging.info("Starting Services...")
    tlm = TelemetryHandler()
    git = GitHandler()
    
    # Present to user what version are we on
    if not IS_IN_SPACE:
        git.git_get_version()
    
    # Do one time full telemetry
    tlm.gather_telemetry(is_full_telemetry=True)
    
    # Take pictures in different iluminations
    camera = CameraHandler()
    artifacts_files_paths = ['telemetry.csv']
    def take_picture_with_led(mode_name,r,g,b,near_or_far,is_use_full_resolution):
        set_led_mode(mode_name,r,g,b)
        path = camera.take_pic(focus=near_or_far,is_use_full_resolution=is_use_full_resolution)
        return path
    R = 150
    G = 170
    B = 50
    take_picture_with_led("OFF",       0,0,0,FAR_FOCUS,  False)
    take_picture_with_led("RED",       R,0,0,FAR_FOCUS,  False)
    take_picture_with_led("GREEN",     0,G,0,FAR_FOCUS,  False)
    take_picture_with_led("BLUE",      0,0,B,FAR_FOCUS,  False)
    artifacts_files_paths.append(take_picture_with_led("WHITE_FAR", R,G,B,FAR_FOCUS,  False))
    im_file_path = take_picture_with_led("WHITE_FAR", R,G,B,FAR_FOCUS,  True)
    artifacts_files_paths.append(camera_preprocess.preprocess(im_file_path))
    im_file_path = take_picture_with_led("WHITE_NEAR",R,G,B,NEAR_FOCUS, True)
    artifacts_files_paths.append(camera_preprocess.preprocess(im_file_path))  
    set_led_mode("OFF")
        
    # Collect artifacts and zip them
    logging.info("Zip artifacts to artifacts.zip file...")
    with zipfile.ZipFile("artifacts.zip", 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in artifacts_files_paths:
            zipf.write(file, os.path.basename(file))
    
    # Finally, update code for next run
    if not IS_IN_SPACE:
        git.git_update_code()
    
    # Say that we are done
    logging.info("Done with this loop")