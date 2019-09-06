import json
import os
from types import SimpleNamespace

project_root = os.getcwd()


# folder names
data_folder = 'data'
save_folder = 'saves'

# file extensions
save_file_ext = '.json'
data_file_ext = '.json'

# full path
saves_path = os.path.join(project_root, save_folder)
data_path = os.path.join(project_root, data_folder)


def get_save_games():
    return [fn[:-len(save_file_ext)] for fn in os.listdir(os.path.join(project_root, save_folder))
            if fn[-len(save_file_ext):] == save_file_ext]


def get_data():
    data = SimpleNamespace()
    for fn in os.listdir(data_path):
        if fn[-len(data_file_ext):] == data_file_ext:
            with open(os.path.join(data_path, fn), 'r') as f:
                data.__setattr__(fn[:-len(data_file_ext)], json.load(f))
    return data


data = get_data()
