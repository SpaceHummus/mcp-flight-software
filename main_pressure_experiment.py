# This script runs pressure measurments constantly to measure the pressure inside chamber during pressure experiment
from git_handler import GitHandler
import logging
from telemetry_handler import TelemetryHandler
from setup_logging import setup_logging
import os
import time

def capture_pressure(tlm):
    tml._get_ms8607_telemetry(is_output_header=False, is_full_telemetry=False)


if __name__ == "__main__":
    setup_logging();

    # Define the services that would be used
    logging.info("Starting Services...")
    tlm = TelemetryHandler()
    
    # Count down before starting to apply pressure
    for countdown in range(10, 0, -1):
        print(countdown)
        capture_pressure(tlm)
        time.sleep(1)  # Sleep for 1 second

    # First few seconds capture every 100 ms
    start_time = time.time()
    while (time.time() < start_time + 20):
        capture_pressure(tlm)
        if time.time() < start_time + 20:
            logging.log("20 sec passed")
        time.sleep(0.1)
    
    # then capture every 5 sec
    while True:
        capture_pressure(tlm)
        time.sleep(0.1)