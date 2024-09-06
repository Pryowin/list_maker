import os
import logging

from datetime import datetime as dt

def config_logging(basedir):
    date_str = dt.now().strftime("%Y-%m-%d")
    log_name = f"list_maker{date_str}.log"

    logging.basicConfig(
        filename=os.path.join(basedir, 'logs///', log_name),  # File name
        filemode='a',            # append to log if it exists
        format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
        datefmt='%Y-%m-%d %H:%M:%S',  # Date format
        level=logging.DEBUG      # Log level
    )