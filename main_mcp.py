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
import time
import bit_error_rate_handler

# Camera parameters
NEAR_FOCUS=100
FAR_FOCUS=200
IS_USE_FULL_RESOLUTION=False

if __name__ == "__main__":
    setup_logging()

    # Define the services that would be used
    logging.info("Starting Services...")
    tlm = TelemetryHandler()
    git = GitHandler()
    
    # Present to user what version are we on
    git.git_get_version()

    # Gather telemetry
    logging.info("Gathering Telemetry...")
    tlm.gather_telemetry()
    
    # Compute hash on a big file
    bit_error_rate_handler.update_hash()
    
    # Take pictures in different iluminations
    camera = CameraHandler()
    def take_picture_with_led(mode_name,r,g,b,near_or_far):
        set_led_mode(mode_name,r,g,b)
        camera.take_pic(focus=near_or_far,is_use_full_resolution=IS_USE_FULL_RESOLUTION)
    take_picture_with_led("OFF",0,0,0,NEAR_FOCUS)
    take_picture_with_led("RED",255,0,0,NEAR_FOCUS)
    take_picture_with_led("GREEN",0,255,0,NEAR_FOCUS)
    take_picture_with_led("BLUE",0,0,255,NEAR_FOCUS)
    take_picture_with_led("WHITE_NEAR",255,255,255,NEAR_FOCUS)
    take_picture_with_led("WHITE_FAR",255,255,255,FAR_FOCUS)
    take_picture_with_led("OFF",0,0,0,FAR_FOCUS)
    
    # Finally, update code for next run
    git.git_update_code()