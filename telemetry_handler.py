'''
This file contains all telemetry services applicable by this board
'''

import adafruit_bme680
import board
import csv
import logging
import time

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
    
    # Gather air quality telemetry
    def _get_bme680_telemetry(self, is_output_header):
        if is_output_header:
            # Just output the header, not the data
            return ['BME680_Temperature[C]','BME680_Gas[Ohm]','BME680_Humidity[%]','BME680_Pressure[hPa]']
    
        # Get the actual data
        try:
            bme680 = adafruit_bme680.Adafruit_BME680_I2C(self.i2c)
            logging.debug("Temperature:%d, Gas: %d ohms, Humidity: %d, Pressure: %d hPa", bme680.temperature,
                          bme680.gas,
                          bme680.humidity, bme680.pressure)
            return [bme680.temperature, bme680.gas, bme680.humidity, bme680.pressure]
        except Exception as e:
            logging.error(
                f"error while reading from the bme680: \n{e}"
            )
            return ['', '', '', ''] # Return empty csv
            
    # Gather how long it took to gather all telemetry
    def _get_telemetry_gather_time(self, is_output_header):
        if is_output_header:
            # Just output the header, not the data
            return ['Telemetry Gather Time [sec]']
            
    execution_time = time.time() - collecting_telemetry_start_time
    return ["{:.1f}".format(execution_time)]    

###################### End of Private Functions to Collect Telemetry ######################

    def gather_telemetry(self, is_output_header=False):
    
        # Mark the time we started to collect telemetry
        self.collecting_telemetry_start_time = time.time()
        
        # Figure out if the telemetry file exists
        if os.path.exists(TELEMETRY_FILE):
            # File doesn't exist, you must output header first
            is_output_header = True
            
        # If starting with header, clean the old file first
        if is_output_header:
            with open(TELEMETRY_FILE, 'w') as f:
                f.truncate(0)

        # Start collecting telemetry, write to file as we go
        row = list()
        with open(TELEMETRY_FILE, 'a', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            row.append(self._get_date_time_state_telemetry(is_output_header))
            row.append(self._get_bme680_telemetry(is_output_header))
            row.append(self._get_telemetry_gather_time(is_output_header))
           
            writer.writerow(row)
        
        if is_output_header:
            # This was the header, run again this time gather telemetry
            return self.gather_telemetry(False)
        else:
            # This was the telemetry, return it
            return row
            

# Test functionality
if __name__ == "__main__":
    tel = TelemetryHandler()
    data = tel.gather_telemetry()
    print(data)