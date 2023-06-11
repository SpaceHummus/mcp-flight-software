''' This file sets up the logging service that is used in this project '''

import logging

def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s [%(levelname)s] %(funcName)s:%(message)s",
        handlers=[
            logging.FileHandler("scp_main.log"),
            logging.StreamHandler()
        ]
    )   
    
if __name__ == "__main__":
    # Demo logging
    setup_logging()
    logging.info("This is an info message")
    logging.debug("This is a debug message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")