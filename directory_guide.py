import os


def data_directory_folder() -> str:
    folder_name = 'storage'
    return folder_name


def log_directory():
    folder_name = data_directory_folder()
    file_path: str = os.path.join(folder_name, 'log.json')
    return file_path