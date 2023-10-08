# This code implements an LED service that keeps track of the ilumination in the chamber and modifies it
import board
from datetime import datetime
import neopixel
import logging
import led_mode_report
from setup_logging import setup_logging
from telemetry_handler import TelemetryHandler
import RPi.GPIO as GPIO
import time

pixels = neopixel.NeoPixel(board.D21, 10,brightness =1)
tel = TelemetryHandler

GPIO.setmode(GPIO.BCM)
LED_ENABLE_PIN = 23
GPIO.setup(LED_ENABLE_PIN,GPIO.OUT)

# Returns current led mode (mode_name,r,g,b)
def get_led_mode():
    return led_mode_report.get_led_mode_from_file()

def set_led_mode(new_r, new_g, new_b, new_mode_name):
    
    # Read what is the current mode
    current_mode_name, current_r, current_g, current_b = get_led_mode()
    
    # Compare current mode to new mode, if they are the same, we are done
    if new_r == current_r and new_g == current_g and new_b == current_b and new_mode_name == current_mode_name:
        
        # If new mode is off, turn off LED power by switching off the GPIO
        if new_mode_name == "off":
            GPIO.output(LED_ENABLE_PIN, False)# Turn Neo pixel enable line
        
        # Nothing more to do, return
        return
        
    # Capture telemtry before making the change so we have reference to compare to
    tel.gather_telemetry()
    
    # Set GPIO switch according to mode
    if new_mode_name == "off":
        GPIO.output(LED_ENABLE_PIN, False)# Turn Neo pixel enable line
    else:
        # Turn on GPIO
        GPIO.output(LED_ENABLE_PIN, True)# Turn on Neo pixel enable line
        
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
    set_led_mode("off",0,0,0)
    time.sleep(0.5)
    set_led_mode("red",255,0,0)
    time.sleep(0.5)
    set_led_mode("green",0,255,0)
    time.sleep(0.5)
    set_led_mode("blue",0,0,255)
    time.sleep(0.5)
    set_led_mode("white",255,255,255)
    time.sleep(0.5)
    set_led_mode("off",0,0,0)


