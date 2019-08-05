# Contains base class for all items
import random

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
    def __init__(self, quality, quality_value=10):
        self.quality = str(quality)
        self.quality_val = quality_value
        self.value = int(10 * quality_value + 10)
        self.equipable = True

    def __del__(self):
        pass

    @classmethod
    def generate(cls):
        qualityity = random.choices(sList, weights=sWeights, k=1)[0]
        qualityity_val = sValue.get(qualityity)
        return cls(qualityity, qualityity_val)

    def __str__(self):
        return f'\nEquipment: \n' \
            f'qualityity: \t\t{self.quality}\n' \
            f'qualityity Value:\t{self.quality_val}\n' \
            f'Item Value:\t\t{self.value}'

    def sell(self):
        # TODO: remove item and add value to player money
        # hero.money += self.value
        # remove from inventory.pop[item_slot]
        # self.del
        pass

    def repair(self):
        # TODO: Add repair function
        # self.max_durability = int(self.max_durability * 0.1)
        pass


class Weapon(Equipment):
    def __init__(self, quality, quality_val, dmg_min=1, dmg_max=4):
        super(Weapon, self).__init__(quality, quality_val)
        self.gear_type = 'Weapon'
        self.name = f'{self.quality} {self.gear_type}'
        self.att_dmg_min = int(dmg_min * self.quality_val)
        self.att_dmg_max = int(dmg_max * self.quality_val)

    def __str__(self):
        return f'\n' \
            f'{self.name}\n' \
            f'Quality Value:\t{self.quality_val}\n' \
            f'Dmg Value:\t\t{self.att_dmg_min} - {self.att_dmg_max}\n' \
            f'Item Value:\t\t{self.value}'

    def calc_weapon_dmg(self):
        damage_output = random.randint(self.att_dmg_min, self.att_dmg_max)
        return damage_output

    def show_stats(self):
        relevant_stats = {
            'Name': self.name,
            'Attack Damage Min': self.att_dmg_min,
            'Attack Damage Max': self.att_dmg_max,
        }
        for k, v in relevant_stats.items():
            print(k, ': ', v)


# TODO: Add Armor Class

# Test code
# w = Weapon.generate()
# print(w)
#
# w.show_stats()
# print('\nTest Damage output:')
# print('weapon damage: ' + str(w.calc_weapon_dmg()), end=', ')
# print(str(w.calc_weapon_dmg()), end=', ')
# print(str(w.calc_weapon_dmg()), end=', ')
# print(str(w.calc_weapon_dmg()), end=', ')
# print(str(w.calc_weapon_dmg()), end=', ')
# print(str(w.calc_weapon_dmg()), end=', ')
# print(str(w.calc_weapon_dmg()))

