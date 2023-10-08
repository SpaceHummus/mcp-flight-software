'''
This file contains all telemetry services applicable by this board
'''

import board
import csv
from datetime import datetime
import itertools
import led_mode_report
import logging
import time
from setup_logging import setup_logging
import os

###################### Import drivers specific for each sensor ######################
# Pressure and humidity sensor library.
from adafruit_ms8607 import MS8607 # If can't import try: sudo pip3 install adafruit-circuitpython-ms8607
# Air quality sensor library.
import adafruit_sgp30 # If can't import try: sudo pip3 install adafruit-circuitpython-sgp30
# Ambient light sensor library.
import adafruit_tsl2591 # If can't import try: sudo pip3 install adafruit-circuitpython-tsl2591
# Current sensor
from barbudor_ina3221.lite import INA3221 # If can't import try: sudo pip3 install barbudor-circuitpython-ina3221

# This is the main telemetry file 
TELEMETRY_FILE = 'telemetry.csv'

class TelemetryHandler:
    i2c = None
    collecting_telemetry_start_time = None

    def __init__(self):
        self.i2c = board.I2C()
        
###################### Private Functions to Collect Telemetry ######################    
    # RTC: I2C Address 0x68
    
    # Gather general information about the date/time and led mode
    def _get_date_time_state_telemetry(self, is_output_header):
        if is_output_header:
            # Just output the header, not the data
            return ['Date & Time','LED Mode']
        
        now = datetime.now()  # current date and time
        date_time = now.strftime("%Y-%m-%d %H:%M:%S")
        mode, *_  = led_mode_report.get_led_mode_from_file()
        return [date_time, mode]
    
    # Gather air pressure, temperature and humidity telemetry
    # I2C Address 0x40, 0x76
    temperature_celsius = -1
    relative_humidity = -1
    def _get_ms8607_telemetry(self, is_output_header): 
        if is_output_header:
            # Just output the header, not the data
            return [
                'MS8670_Pressure[hPa]',
                'MS8670_Temperature[C]',
                'MS8670_RelativeHumidity[%]',
                ]
    
        # Get the actual data
        try:
            ms8607 = MS8607(self.i2c)
            logging.debug("\nPressure: %5.1f[hPa], Temperature: %3.1f[C], Relative Humidity: %3.0f%%", 
                ms8607.pressure, ms8607.temperature, ms8607.relative_humidity)
            self.temperature_celsius = ms8607.temperature
            self.relative_humidity = ms8607.relative_humidity
            return [
                "{:<5.1f}".format(ms8607.pressure),
                "{:<3.1f}".format(ms8607.temperature), 
                "{:<3.0f}".format(ms8607.relative_humidity), 
                ]
        except Exception as e:
            logging.error(
                f"error while reading from MS8607: \n{e}"
            )
            return ['', '', ''] # Return empty csv
    
    # Gather gas composition telemetry, This sensor takes ~10 seconds to warm up
    # Set temperature and relative humidity for better percision 
    # More information about operation: https://learn.adafruit.com/adafruit-sgp30-gas-tvoc-eco2-mox-sensor/circuitpython-wiring-test
    # I2C Address 0x58
    sgp30 = None
    sgp30_init_time = None
    def _init_sgp30_telemetry(self, temperature_celsius=22.1, relative_humidity=44):
        self.sgp30_init_time = time.time()
        try:
            # Create library object on our I2C port
            self.sgp30 = adafruit_sgp30.Adafruit_SGP30(self.i2c)

            # TDOO: Switch this with adaptive baseline 
            self.sgp30.set_iaq_baseline(0x8973, 0x8AAE) 
            
            # Calibration is better when temperature and relative humidity is given
            if (isinstance(temperature_celsius, (int, float)) and 
                relative_humidity>0): # If no telemetry was provided, relative_humidity will be -1. This clause prevents us from initializing using bad data
                logging.debug("Init SGP30 with temp & humidity.\nTemperature: %3.1f[C], Relative Humidity: %3.0f%%", 
                    temperature_celsius, relative_humidity)
                self.sgp30.set_iaq_relative_humidity(
                    celsius=temperature_celsius, 
                    relative_humidity=relative_humidity
                    )
        except Exception as e:
            logging.error(
                f"error while initializing SGP30: \n{e}"
            )
        
    def _get_sgp30_telemetry(self, is_output_header):
        if is_output_header:
            # Just output the header, not the data
            return [
                'SGP30_eCO2[ppm]',
                'SGP30_TVOC[ppb]',
                ]
        
        # Make sure that enough time passed from init such that sensor is accurate 
        time_passed = time.time() - self.sgp30_init_time
        min_wait_time_sec = 15
        if (time_passed < min_wait_time_sec):
            # Not enugh time passed, try again
            time.sleep(min_wait_time_sec-time_passed)
    
        # Get the actual data
        try:
            
            logging.debug("\neCO2: %4.0f[ppm], TVOC: %4.1f", 
                self.sgp30.eCO2, self.sgp30.TVOC)
            return [
                "{:<4.0f}".format(self.sgp30.eCO2),
                "{:<4.0f}".format(self.sgp30.TVOC) 
                ]
        except Exception as e:
            logging.error(
                f"error while reading from SGP30: \n{e}"
            )
            return ['', ''] # Return empty csv
    
    # Gather ambient light intensity
    # I2C Address 0x28 and 0x29
    def _get_tsl2591_telemetry(self, is_output_header):
        if is_output_header:
            # Just output the header, not the data
            return [
                'TSL_OverallLight[lux]',
                ]
    
        # Get the actual data
        try:
            tsl = adafruit_tsl2591.TSL2591(self.i2c)
            logging.debug("Overall Light: %5.2f[lux]", 
                tsl.lux)
            return [
                "{:<5.2f}".format(tsl.lux)
                ]
        except Exception as e:
            logging.error(
                f"error while reading from TSL2591: \n{e}"
            )
            return [''] # Return empty csv
    
    # Gather current and power consumption.
    # I2C Address 0x41
    def _probe_ina3221_telemetry(self, is_output_header):
        if is_output_header:
            # Just output the header, not the data
            return [
                'INA_Current1[mA]','INA_Voltage1[V]','INA_Current2[mA]','INA_Voltage2[V]','INA_Current3[mA]','INA_Voltage3[V]',
                ]
                
        # Get the actual data
        try:
            # Init device
            ina3221 = INA3221(self.i2c, shunt_resistor=(0.05,0.05,0.05), i2c_addr=0x41)
            
            # Enable all 3 channels.
            ina3221.enable_channel(1)
            ina3221.enable_channel(2)
            ina3221.enable_channel(3)
            
            # Read data
            current1 = ina3221.current(1)*1000
            voltage1 = ina3221.bus_voltage(1)
            current2 = ina3221.current(2)*1000
            voltage2 = ina3221.bus_voltage(2)
            current3 = ina3221.current(3)*1000
            voltage3 = ina3221.bus_voltage(3)
            
            # Log and return
            logging.debug("Ch1: Current: %3.0f[mA], Voltage: %1.2f[V]",current1,voltage1)
            logging.debug("Ch2: Current: %3.0f[mA], Voltage: %1.2f[V]",current2,voltage2)
            logging.debug("Ch3: Current: %3.0f[mA], Voltage: %1.2f[V]",current3,voltage3)
            return [
                "{:<3.0f}".format(current1),
                "{:<1.2f}".format(voltage1),
                "{:<3.0f}".format(current2),
                "{:<1.2f}".format(voltage2),
                "{:<3.0f}".format(current3),
                "{:<1.2f}".format(voltage3),
                ]
        except Exception as e:
            logging.error(
                f"error while reading from INA3221: \n{e}"
            )
            return [''] # Return empty csv
            
    # Understand what are the active I2C Devices
    def _probe_i2c_devices(self,is_output_header):
        if is_output_header:
            # Just output the header, not the data
            return ['Active I2C Devices [Hex]']
    
        # Probe
        active_i2c_addresses = self.i2c.scan()
        
        # Convert to hex
        hex_strings = [hex(num) for num in active_i2c_addresses]

        # Join the hexadecimal strings into a single string
        active_i2c_devices_str = ' '.join(hex_strings)
        logging.debug("\nActive I2C Devices: " + active_i2c_devices_str)
        
        # Self check which devices are connected 
        def is_address_active(address, device_name):
            if address in active_i2c_devices_str:
                logging.debug(f"{address} CONNECTED     ({device_name})")
            else:
                logging.debug(f"{address} NOT CONNECTED ({device_name})")
        is_address_active("0x28","TSL2591 Ilumination (1st address)")
        is_address_active("0x29","TSL2591 Ilumination (2nd address)")
        is_address_active("0x40","MS8607 Temperture & Humidity (1st address)")
        is_address_active("0x76","MS8607 Temperture & Humidity (2nd address)")
        is_address_active("0x41","INA3221 Current sensor")
        is_address_active("0x58","SPG30 Gas Sensor")
        is_address_active("0x68","RTC")
        
              
        return [active_i2c_devices_str]
            
    # Gather how long it took to gather all telemetry
    def _get_telemetry_gather_time(self, is_output_header):
        if is_output_header:
            # Just output the header, not the data
            return ['TelemetryCycleTime[sec]']
            
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
            row.append(self._get_ms8607_telemetry(is_output_header))
            self._init_sgp30_telemetry(self.temperature_celsius, self.relative_humidity) # Init sensor with the measured data
            row.append(self._get_tsl2591_telemetry(is_output_header))
            row.append(self._probe_ina3221_telemetry(is_output_header))
            row.append(self._get_sgp30_telemetry(is_output_header))
            row.append(self._probe_i2c_devices(is_output_header))
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