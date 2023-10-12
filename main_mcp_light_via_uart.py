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
import camera_handler
import camera_preprocess
import time
import zipfile
import os
import led_mode_report
import logging
import serial

uart_port = '/dev/ttyS0'
baud_rate = 19200  # Adjust based on your UART device configuration



# Camera parameters
NEAR_FOCUS=600
FAR_FOCUS=1000
IS_USE_FULL_RESOLUTION=True
IS_IN_SPACE=True

if __name__ == "__main__":
    # Open the UART port
    ser = serial.Serial(uart_port, baud_rate, timeout=0)

    #setup_logging()
    git = GitHandler()
    
    logging.basicConfig(level=logging.ERROR)  
    
    R = 150
    G = 170
    B = 50
    set_led_mode('',R,G,B)
    
    tlm = TelemetryHandler()
    s = tlm.gather_telemetry(is_full_telemetry=True)
    
    s = str(s)
    print(len(s))
    print(s)
    ser.write(s.encode('utf-8') + b'\n')
   
    # Finally, update code for next run
    if not IS_IN_SPACE:
        git.git_update_code()
    