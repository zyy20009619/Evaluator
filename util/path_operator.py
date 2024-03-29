import os


def create_file_path(folder_path, file_name):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return os.path.join(folder_path, file_name)

def create_dir_path(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path