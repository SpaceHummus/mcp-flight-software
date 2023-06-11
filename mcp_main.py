'''
This is the main function to be executed by linux computer.
It runs as a "single shot". Collects telemetry, decides what is the next thing to do, then dies.
'''
from git_handler import GitHandler
import logging
from telemetry_handler import TelemetryHandler
from setup_logging import setup_logging

if __name__ == "__main__":
    setup_logging()

    # Define the services that would be used
    logging.info("Starting Services...")
    tlm = TelemetryHandler()
    git = GitHandler()
    
    # Present to user what version are we on
    git.git_get_version()

    # Gather telemetry
    logging.info("Starting Services...")
    tlm.gather_telemetry()
    
    # Finally, update code for next run
    git.git_update_code()