# Contains base class for equipable items
import random
import string

sWeights = (8, 44, 22, 18, 8)
sList = ['Rusty', 'Common',
         'Great', 'Magical',
         'Legendary']
sValue = {'Rusty': 0.9, 'Common': 1,
          'Great': 1.25, 'Magical': 1.6,
          'Legendary': 2}


class Consumable:
    pass


class Equipment:
    def __init__(self, quality, quality_value=10, etype='Weapon', value=0,
                 max_durability=10, strength=0, dexterity=0, intelligence=0,
                 max_hp=0, defense=0, att_dmg_min=0, att_dmg_max=0, damage=0,
                 crit_chance=0, crit_multiplier=0):
        self.quality = str(quality)
        self.quality_val = quality_value
        self.value = value + int(10 * quality_value + 10)
        self.max_durability = max_durability
        self.durability = self.max_durability

        self.type = etype
        self._equipable_slot = 'main_hand'

        self.str = strength
        self.dex = dexterity
        self.int = intelligence
        self.max_hp = max_hp
        self.defense = defense
        self.att_dmg_min = att_dmg_min
        self.att_dmg_max = att_dmg_max
        self.damage = damage
        self.crit_chance = crit_chance
        self.crit_muliplier = crit_multiplier

        self._max_left = max(len(k) for k in self.__dict__.keys()) + 10

    @classmethod
    def generate(cls):
        qualityity = random.choices(sList, weights=sWeights, k=1)[0]
        qualityity_val = sValue.get(qualityity)
        return cls(qualityity, qualityity_val)

    def __repr__(self):
        # max_left = max(len(k) for k in self.__dict__.keys()) + 7
        return '\n'.join(
            [f"{k.title()}: {str(v).rjust(self._max_left - len(k), ' ')}"
             for k, v in self.__dict__.items()])

    def __str__(self):
        # max_left = max(len(k) for k in self.__dict__.keys()) + 7
        return '\n'.join(
            [f"{k.title()}: {str(v).rjust(self._max_left - len(k), ' ')}"
             for k, v in self.__dict__.items() if v and k[0] != '_'])

    def sell(self):
        # TODO: remove item and add value to player money
        # hero.money += self.value
        # remove from inventory.pop[item_slot]
        # self.del
        pass

    def repair(self):
        # TODO: Add repair function
        self.max_durability = int(self.max_durability * 0.9)


class Weapon(Equipment):
    def __init__(self, quality, quality_val):
        super(Weapon, self).__init__(quality, quality_val, etype='Weapon', damage=5)

    @classmethod
    def generate(cls):
        qualityity = random.choices(sList, weights=sWeights, k=1)[0]
        qualityity_val = sValue.get(qualityity)
        return cls(qualityity, qualityity_val)

    def calc_weapon_dmg(self):
        damage_output = random.randint(self.att_dmg_min, self.att_dmg_max)
        return damage_output

class Armor(Equipment):
    def __init__(self, quality, quality_val):
        super(Armor, self).__init__(quality, quality_val, etype='Armor', defense=5)

    @classmethod
    def generate(cls):
        qualityity = random.choices(sList, weights=sWeights, k=1)[0]
        qualityity_val = sValue.get(qualityity)
        return cls(qualityity, qualityity_val)


# Code designed to generate item variation
def generate_quality():
    return random.choices(list(sValue.keys()), weights=sWeights, k=1)[0]


def generate_item_variable_str(string_length=5):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.sample(letters, string_length))


def create_random_item(class_type=1):
    """Generates an instance of the selected class"""
    if class_type == 1:
        item_variable = Weapon.generate()
        return item_variable

    elif class_type == 2:
        item_variable = Armor.generate()
        return item_variable


def create_random_equipable_item(how_many=1, etype=random.randint(1, 2)):
    for i in range(0, how_many):
        x = create_random_item(etype)
        return x
