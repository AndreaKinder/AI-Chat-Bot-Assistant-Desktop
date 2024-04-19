import json
import os
from src import directory_guide

folder_name = directory_guide.data_directory_folder()

file_path = directory_guide.log_directory()


def capture_log(us, passwd):
    data = {'us': us, 'passwd': passwd}
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    with open(file_path, 'w') as file:
        json.dump(data, file)


def read_log():
    with open(file_path, 'r') as log:
        log_data = json.load(log)
        return log_data['us'], log_data['passwd']