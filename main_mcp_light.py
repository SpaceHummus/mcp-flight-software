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
    
    tlm = TelemetryHandler()
    s = tlm.gather_telemetry(is_full_telemetry=True)
    
    print(len(s))
    print(s)
   
    # Finally, update code for next run
    if not IS_IN_SPACE:
        git.git_update_code()
    