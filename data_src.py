import json
import os
from types import SimpleNamespace
import random

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

if save_folder not in os.listdir(project_root):
    os.mkdir(save_folder)


def get_save_games():
    return [fn[:-len(save_file_ext)] for fn in os.listdir(os.path.join(project_root, save_folder))
            if fn[-len(save_file_ext):] == save_file_ext]


def get_data():
    f_data = {}
    for fn in os.listdir(data_path):
        if fn[-len(data_file_ext):] == data_file_ext:
            with open(os.path.join(data_path, fn), 'r') as f:
                f_data[fn[:-len(data_file_ext)]] = json.load(f)
    return f_data


data = get_data()


def save_to_json(s_data, file_name):
    fn = os.path.join(data_path, file_name+data_file_ext)
    with open(fn, 'w') as f:
        json.dump(s_data, f, indent=4)

#
# def get_attack_setup(item):
#     atks_loc = item.get('attack_setup').split('/')
#     return data.attack_setups[atks_loc[0]][atks_loc[1]]


def get_keys_from_loc_str(data, key_str):
    key_list = key_str.split('/')
    keys = []
    for key in key_list:
        if key == 'rng':
            key = random.choice(list(data.keys()))
        keys.append(key)
        data = data[key]
    return keys


def get_data_from_keys(data, keys):
    for key in keys:
        data = data[key]
    return data


def get_data_from_loc_str(data, loc_str):
    keys = get_keys_from_loc_str(data, loc_str)
    return get_data_from_keys(data, keys)


def search_loc(search_loc, condition_loc, condition_value, result='entry', data=data):
    results = []
    haystack = get_data_from_loc_str(data, search_loc)

    for entry in haystack.items():
        entry_condition = get_data_from_loc_str(entry[1], condition_loc)
        if entry_condition == condition_value:
            if result == 'entry':
                results.append(entry[1])
            elif result == 'key':
                results.append(entry[0])
            if result == 'both':
                results.append(entry)
    return results
