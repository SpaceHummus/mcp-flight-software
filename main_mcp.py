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
    
    # Take color pictures
    camera = CameraHandler()
    set_led_mode("off")
    time.sleep(1)
    set_led_mode("red",255,0,0)
    time.sleep(1)
    set_led_mode("green",0,255,0)
    time.sleep(1)
    set_led_mode("blue",0,0,255)
    time.sleep(1)
    set_led_mode("off")
    
    # Finally, update code for next run
    git.git_update_code()