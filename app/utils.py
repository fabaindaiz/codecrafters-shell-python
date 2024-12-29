import os

HOME = os.getenv("HOME")
PATH = os.getenv("PATH").split(":")

def search_file_in_path(file_name):
    for path in PATH:
        if os.path.isfile(f"{path}/{file_name}"):
            return f"{path}/{file_name}"
    return None