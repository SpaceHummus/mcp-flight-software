# This code implements an LED service that keeps track of the ilumination in the chamber and modifies it
import board
from datetime import datetime
import neopixel
import logging
import led_mode_report
from setup_logging import setup_logging
from telemetry_handler import TelemetryHandler
import time

pixels = neopixel.NeoPixel(board.D21, 10,brightness =1)
tel = TelemetryHandler

# Returns current led mode (mode_name,r,g,b)
def get_led_mode():
    # Todo, read from file

    return led_mode_report.get_led_mode_from_file()

def set_led_mode(new_r, new_g, new_b, new_mode_name):
    
    # Read swhat is the current mode
    current_mode_name, current_r, current_g, current_b = get_led_mode()
    
    # Compare current mode to new mode, if they are the same, we are done
    if new_r == current_r and new_g == current_g and new_b == current_b and new_mode_name == current_mode_name:
        
        # If new mode is off, turn off LED power by switching off the GPIO
        if new_mode_name == "off":
            print("TODO") # Todo
        
        # Nothing more to do, return
        return
        
    # Capture telemtry before making the change so we have reference to compare to
    tel.gather_telemetry()
    
    # Set GPIO switch according to mode
    if new_mode_name == "off":
        print("TODO") # Todo, trurn GPIO
    else:
        # Turn on GPIO
        print("TODO")
        
        # Let power ramp up
        time.sleep(0.1)
        
        # Set Neopixel values
        pixels.fill((new_r, new_g, new_b))
        pixels.show()
        
    led_mode_report.set_led_mode_to_file(new_mode_name, new_r, new_g, new_b)

    # Capture telemtry right after making the change so we have reference to compare to
    tel.gather_telemetry()
        
    

# Test functionality
if __name__ == "__main__":
    setup_logging()
    
    # Todo




