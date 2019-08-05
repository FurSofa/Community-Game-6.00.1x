# Code designed to generate item variation

import random
import string

inventory = []
used_item_variable_str = []

sWeights = (8, 44, 22, 18, 8)
sList = ['Rusty', 'Common', 'Great', 'Magical', 'Legendary']
sValue = {'Rusty': 0.9, 'Common': 1, 'Great': 1.25, 'Magical': 1.6, 'Legendary': 2}

qualityity = random.choices(list(sValue.keys()), weights=sWeights, k=1)
qualityity_val = sValue.get(qualityity[0])

def generate_qualityity():
    return random.choices(list(sValue.keys()), weights=sWeights, k=1)



def generate_item_variable_str(string_length=5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, string_length))


def create_random_item(item_variable='aaaaa', class_type=1):
    """Generates an instance of the selected class"""
    if class_type == 1:
        item_variable = Weapon.generate()
        return item_variable

    elif class_type == 2:
        item_variable = Armor.generate()
        return item_variable


def create_random_equipable_item(how_many=1):
    for i in range(0, how_many):
        x = create_random_item(generate_item_variable_str(), random.randint(1, 2))
        inventory.append(x)
        print(x)
