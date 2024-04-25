import os


def create_data_log_file():
    """
    Creates a data log file if it does not already exist.

    This function creates a data log file in the "data-log" directory with the name "log.txt". If the "data-log" directory does not exist, it is created. If the file already exists, no action is taken.

    Parameters:
        None

    Returns:
        None
    """
    file_directory = "data-log"
    new_file = "log.txt"
    file_path = os.path.join(file_directory, new_file)
    
    if not os.path.exists(file_directory):
        os.mkdir(file_directory)
    
    if not os.path.exists(file_path):
        open(file_path, "x")
    
    print("sucessfully created")
    