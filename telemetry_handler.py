'''
This file contains all telemetry services applicable by this board
'''

import adafruit_bme680 # If can't import try: sudo pip3 install adafruit-circuitpython-bme680
import adafruit_sgp30 # If can't import try: sudo pip3 install adafruit-circuitpython-sgp30
import board
import csv
from datetime import datetime
import itertools
import logging
import time
from setup_logging import setup_logging
import os

# This is the main telemetry file 
TELEMETRY_FILE = 'telemetry.csv'

class TelemetryHandler:
    i2c = None
    collecting_telemetry_start_time = None

    def __init__(self):
        self.i2c = board.I2C()
        
###################### Private Functions to Collect Telemetry ######################    
    
    # Gather general information about the date/time and state
    def _get_date_time_state_telemetry(self, is_output_header):
        if is_output_header:
            # Just output the header, not the data
            return ['Date & Time','Logic State']
        
        now = datetime.now()  # current date and time
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        state = 'Not Implemented'
        return [date_time, state]
    
    # Gather air pressure, temperature and humidity telemetry
    def _get_bme680_telemetry(self, is_output_header, bme_address=118): # Addresses: 0x77 - 119 (default) or 0x76 - 118
        if is_output_header:
            # Just output the header, not the data
            return [
                'BME680_Pressure[hPa]',
                'BME680_Temperature[C]',
                'BME680_Humidity[%]',
                'BME680_Gas[KOhm]',
                ]
    
        # Get the actual data
        try:
            bme680 = adafruit_bme680.Adafruit_BME680_I2C(self.i2c, bme_address) # Addresses: 0x77 - 119 (default) or 0x76 - 118
            logging.debug("\nPressure: %5.1f hPa, Temperature:%3.1f, Humidity: %3.0f%%, Gas: %3.1f KOhms", 
                bme680.pressure, bme680.temperature, bme680.humidity,  bme680.gas/1000)
            return [
                "{:<5.1f}".format(bme680.pressure),
                "{:<3.1f}".format(bme680.temperature), 
                "{:<3.0f}".format(bme680.humidity), 
                "{:<3.1f}".format(bme680.gas/1000)
                ]
        except Exception as e:
            logging.error(
                f"error while reading from the bme680: \n{e}"
            )
            return ['', '', '', ''] # Return empty csv
    
    # Gather gas composition telemetry, This sensor takes ~10 seconds to warm up
    # Set temperture and relative humidity for better percision 
    # More information about operation: https://learn.adafruit.com/adafruit-sgp30-gas-tvoc-eco2-mox-sensor/circuitpython-wiring-test
    sgp30 = None
    sgp30_init_time = None
    def _init_sgp_telemetry(self, celsius=22.1, relative_humidity=44):
        # Create library object on our I2C port
        sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)

        # TDOO: Switch this with adaptive baseline 
        sgp30.set_iaq_baseline(0x8973, 0x8AAE) 
        
        # Calibration is better when temperture and relative humidity is given
        sgp30.set_iaq_relative_humidity(celsius, relative_humidity)
        
        self.sgp30_init_time = time.time()
        
    def _get_sgp_telemetry(self, is_output_header):
        if is_output_header:
            # Just output the header, not the data
            return [
                'SGP_eCO2[ppm]',
                'SGP_TVOC[ppb]',
                ]
        
        # Make sure that enough time passed from init such that sensor is accurate 
        time_passed = time.time() - sgp30_init_time
        if (time_passed < 10):
            # Not enugh time passed, try again
            time.sleep(10-time_passed)
    
        # Get the actual data
        try:
            
            logging.debug("\neCO2: %4.0f ppm, TVOC:%4.1f", 
                sgp30.eCO2, sgp30.TVOC)
            return [
                "{:<4.0f}".format(sgp30.eCO2),
                "{:<4.0f}".format(sgp30.TVOC) 
                ]
        except Exception as e:
            logging.error(
                f"error while reading from the SGP: \n{e}"
            )
            return ['', ''] # Return empty csv
            
    # Active I2C Devices
    def _probe_i2c_devices(self,is_output_header):
        if is_output_header:
            # Just output the header, not the data
            return ['Active I2C Devices [Hex]']
    
        # Probe
        active_i2c_addresses = self.i2c.scan()
        
        # Convert to hex
        hex_strings = [hex(num) for num in active_i2c_addresses]

        # Join the hexadecimal strings into a single string
        result = ' '.join(hex_strings)
        logging.debug("\nActive I2C Devices: " + result)
        
        return [result]
            
    # Gather how long it took to gather all telemetry
    def _get_telemetry_gather_time(self, is_output_header):
        if is_output_header:
            # Just output the header, not the data
            return ['Telemetry Gather Time [sec]']
            
        execution_time = time.time() - self.collecting_telemetry_start_time
        return ["{:.1f}".format(execution_time)]    

###################### End of Private Functions to Collect Telemetry ######################

    def gather_telemetry(self, is_output_header=False):
    
        # Mark the time we started to collect telemetry
        self.collecting_telemetry_start_time = time.time()
        
        # Figure out if the telemetry file exists
        if not os.path.exists(TELEMETRY_FILE):
            # File doesn't exist, you must output header first
            is_output_header = True
            logging.info("Telemetry file doesn't exist, creating it")
            
        # If starting with header, clean the old file first
        if is_output_header:
            with open(TELEMETRY_FILE, 'w') as f:
                f.truncate(0)

        # Start collecting telemetry, write to file as we go
        row = list()
        with open(TELEMETRY_FILE, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            row.append(self._get_date_time_state_telemetry(is_output_header))
            row.append(self._get_bme680_telemetry(is_output_header, 118))
            self._init_sgp_telemetry(22.1, 44)
            row.append(self._get_bme680_telemetry(is_output_header, 119))
            row.append(self._probe_i2c_devices(is_output_header))
            row.append(self._get_sgp_telemetry(is_output_header))
            row.append(self._get_telemetry_gather_time(is_output_header))
            
            # Flatten the list
            row = list(itertools.chain.from_iterable(row))
           
            #logging.info(row) # Log the content of the telemetry
            writer.writerow(row)
        
        if is_output_header:
            # This was the header, run again this time gather telemetry
            return self.gather_telemetry(False)
        else:
            # This was the telemetry, return it
            return row
            

# Test functionality
if __name__ == "__main__":
    setup_logging()
    tel = TelemetryHandler()
    data = tel.gather_telemetry()
    print(data)