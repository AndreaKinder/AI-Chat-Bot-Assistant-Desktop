import os
from window.window_log import create_window_log
from src.directory_guide import log_directory

file_path = log_directory()


def check_directory(directory):
    if os.path.exists(directory) and os.path.isdir(directory):
        return True
    else:
        return False


def check_file_true():
    print("The directory exists and contains a JSON file.")


def check_file_false():
    print("The directory does not exist or does not contain a JSON file.")


def check_file_log():
    directory = os.path.dirname(file_path)
    if check_directory(directory):
        if os.path.isfile(file_path):
            check_file_true()
            return True
        else:
            check_file_false()
            create_window_log()
            return False
    else:
        check_file_false()
        create_window_log()
        return False
