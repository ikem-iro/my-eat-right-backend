import logging
import sys
import os
from .file_config_utils import create_data_log_file

create_data_log_file()

file_directory = "data-log"
new_file = "log.txt"
file_path = os.path.join(file_directory, new_file)


logger = logging.getLogger()


formatter = logging.Formatter(fmt="%(asctime)s - %(levelname)s - %(message)s")



file_handler = logging.FileHandler(file_path)

file_handler.setFormatter(formatter)

logger.handlers = [file_handler]


logger.setLevel(logging.INFO)
