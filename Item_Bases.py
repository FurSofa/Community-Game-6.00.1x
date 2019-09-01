# Contains base class for equipable items
import random
from vfx import *
import string
from x_Attack_Setups import weapon_setups

sWeights = (6, 44, 28, 18, 4)
sList = ['Rusty', 'Common',
         'Great', 'Magical',
         'Legendary']
sValue = {'Rusty': 0.8, 'Common': 1,
          'Great': 1.5, 'Magical': 2,
          'Legendary': 2.5}


class Consumable:
    pass


class Equipment:
    def __init__(self, quality, quality_value=1, etype='none', equipable_slot='none', value=0,
                 max_durability=10, strength=0, dexterity=0, intelligence=0,
                 max_hp=0, defense=0, att_dmg_min=0, att_dmg_max=0, damage=0,
                 crit_chance=0, crit_multiplier=0):
        self.quality = str(quality)
        self.quality_val = quality_value
        self.value = value + int(10 * quality_value + 10)
        self.max_durability = max_durability
        self.durability = self.max_durability
        self.enchants = []

        self.type = etype
        self.equipable_slot = equipable_slot

        self.str = round(strength * self.quality_val)
        self.dex = round(dexterity * self.quality_val)
        self.int = round(intelligence * self.quality_val)
        self.max_hp = round(max_hp * self.quality_val)
        self.defense = round(defense * self.quality_val)
        self.att_dmg_min = round(att_dmg_min * self.quality_val)
        self.att_dmg_max = round(att_dmg_max * self.quality_val)
        self.damage = round(damage * self.quality_val)
        self.crit_chance = round(crit_chance * self.quality_val)
        self.crit_multiplier = round(crit_multiplier * self.quality_val)

        self.base_stats = {
            'vit': 0,
            'dex': round(dexterity * self.quality_val),
            'str': round(strength * self.quality_val),
            'int': round(intelligence * self.quality_val),
            'agility': 1,
            'toughness': 1,
        }
        self.stats = {
            'max_hp': round(max_hp * self.quality_val),
            'max_mana': 10,
            'armor': round(defense * self.quality_val),
            'magic_resistance': 0,
            'speed': 0,
            'dodge': 0,
            'crit_chance': round(crit_chance * self.quality_val),
            'crit_dmg': round(crit_multiplier * self.quality_val),
            'elemental_resistance': 5,
            'wpn_dmg': round(damage * self.quality_val),
        }


    @classmethod
    def generate(cls, quality='Common', quality_val=1, etype='Weapon', equipable_slot='Main Hand', value=0,
                 max_durability=10, strength=0, dexterity=0, intelligence=0,
                 max_hp=0, defense=0, att_dmg_min=0, att_dmg_max=0, damage=0,
                 crit_chance=0, crit_multiplier=0):
        quality = random.choices(sList, weights=sWeights, k=1)[0]
        quality_val = sValue.get(quality)
        return cls(quality, quality_val, etype, equipable_slot, value,
                   max_durability, strength, dexterity, intelligence,
                   max_hp, defense, att_dmg_min, att_dmg_max, damage,
                   crit_chance, crit_multiplier)

    def __repr__(self):
        _max_left = max(len(k) for k in self.__dict__.keys()) + 10
        return '\n'.join(
            [f"{k.title()}: {str(v).rjust(_max_left - len(k), ' ')}"
             for k, v in self.__dict__.items()])

    def show_stats(self):
        name = f'{self.quality} {self.type}'
        slot = f'{self.equipable_slot.title():>9}'
        dmg = f'{self.att_dmg_min:>3}-{self.att_dmg_max:<3}'
        line2_left = f'Dur: {self.durability:>2}/{self.max_durability:<2} '
        line2_right = f'Damage: {dmg}'
        return f'{name:<15}{slot:>15}\n{line2_left:<15}{line2_right:>15}\n'

    def __str__(self):
        return f'{self.quality} {self.type}: {self.equipable_slot}'

    def item_card(self):

        if self.type == 'Weapon':
            # Line 1
            line_1_left = f'{self.quality} {self.type}'
            line_1_right = f'{self.equipable_slot}'

            # Line 2
            line_2_left = f'Dur: {self.durability:>2}/{self.max_durability:<2}'
            line_2_right = f'Damage: {self.att_dmg_min:>3}-{self.att_dmg_max:<3}'

            # Line 3
            line_3_left = " " * 15
            line_3_right = " " * 15
            if self.enchants[0]:
                for enchant, value in self.enchants[0]:
                    chant1 = f'{enchant}: {value}'
                    line_3_left = f'{chant1}'
            if self.enchants[1]:
                for enchant, value in self.enchants[1]:
                    chant2 = f'{enchant}: {value}'
                    line_3_right = f'{chant2}'


            # Combine L an R lines
            line_1 = f'{line_1_left}{line_1_right:>{30 - len(line_1_left)}}'
            line_2 = f'{line_2_left}{line_2_right:>{30 - len(line_2_left)}}'
            line_3 = f'{line_3_left}{line_3_right:>{30 - len(line_3_left)}}'
            return [line_1, line_2, line_3]

        elif self.type == 'Armor':
            # Line 1
            line_1_left = f'{self.quality} {self.type}'
            line_1_right = f'{self.equipable_slot}'

            # Line 2
            line_2_left = f'Dur: {self.durability:>2}/{self.max_durability:<2}'
            line_2_right = f'Defense: {self.defense:>3}'

            # Line 3
            if self.enchant_1:
                line_3_left = f'{self.enchant_1}{self.enchant_1_val}'
            else:
                line_3_left = " " * 15
            if self.enchant_2:
                line_3_right = f'{self.enchant_2}{self.enchant_2_val}'
            else:
                line_3_right = " " * 15

            # Combine L an R lines
            line_1 = f'{line_1_left}{line_1_right:>{30 - len(line_1_left)}}'
            line_2 = f'{line_2_left}{line_2_right:>{30 - len(line_2_left)}}'
            line_3 = f'{line_3_left}{line_3_right:>{30 - len(line_3_left)}}'
            return [line_1, line_2, line_3]

        elif self.type == 'Jewelry':
            # Line 1
            line_1_left = f'{self.quality} {self.type}'
            line_1_right = f'{self.equipable_slot}'

            # Line 2
            if self.enchant_1:
                line_2_left = f'{self.enchant_1}{self.enchant_1_val}'
            else:
                line_2_left = " " * 15
            if self.enchant_2:
                line_2_right = f'{self.enchant_2}{self.enchant_2_val}'
            else:
                line_2_right = " " * 15

            # Line 3
            if self.enchant_1:
                line_3_left = f'{self.enchant_3}{self.enchant_3_val}'
            else:
                line_3_left = " " * 15
            if self.enchant_2:
                line_3_right = f'{self.enchant_4}{self.enchant_4_val}'
            else:
                line_3_right = " " * 15

            # Combine L an R lines
            line_1 = f'{line_1_left}{line_1_right:>{30 - len(line_1_left)}}'
            line_2 = f'{line_2_left}{line_2_right:>{30 - len(line_2_left)}}'
            line_3 = f'{line_3_left}{line_3_right:>{30 - len(line_3_left)}}'
            return [line_1, line_2, line_3]
        else:
            return ['                              ',
                    '            Empty             ',
                    '                              ']

    def info(self):
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

    def hp_bar(self, length=5, f_color=bcolors.OKGREEN, m_color=bcolors.FAIL,
               f_char='#', m_char='-', no_color=True, border='|'):
        '''
        returns a string of an hp_bar for current hp / max hp
        :param no_color: bool
        :param length: int: length of the bar without border - number of chars
        :param f_color: color code : for filled ticks
        :param m_color: color code : for missing ticks
        :param f_char: str: char to display for filled ticks
        :param m_char: str: char to be displayed for not filled ticks
        :param border: added at the beginning and the ned of the string
        :return: hp bar as string
        '''
        bar = BarGFX(self.durability, self.max_durability, length=length, f_color=f_color, m_color=m_color,
                     f_char=f_char, m_char=m_char)
        return bar.bar_str(no_color=no_color, border=border)


class Weapon(Equipment):
    def __init__(self, quality, quality_val=1, etype='Weapon', equipable_slot='Main Hand', value=0,
                 max_durability=10, strength=0, dexterity=0, intelligence=0,
                 max_hp=0, defense=0, att_dmg_min=1, att_dmg_max=3, damage=0,
                 crit_chance=1, crit_multiplier=4,
                 attack_name='single_attack_setup',
                 attack_setup=weapon_setups['single_attack_setup']):
        super(Weapon, self).__init__(quality, quality_val, etype, equipable_slot, value,
                                     max_durability, strength, dexterity, intelligence,
                                     max_hp, defense, att_dmg_min, att_dmg_max, damage,
                                     crit_chance, crit_multiplier)
        self.attack_name = attack_name
        self.attack_setup = attack_setup

    @classmethod
    def generate(cls, quality='Common', quality_val=1, etype='Weapon', equipable_slot='Main Hand', value=0,
                 max_durability=10, strength=0, dexterity=0, intelligence=0,
                 max_hp=0, defense=0, att_dmg_min=1, att_dmg_max=2, damage=0,
                 crit_chance=0, crit_multiplier=0,
                 attack_name='single_attack_setup',
                 attack_setup=weapon_setups['single_attack_setup']
                 ):
        return cls(quality, quality_val, etype, equipable_slot, value,
                   max_durability, strength, dexterity, intelligence,
                   max_hp, defense, att_dmg_min, att_dmg_max, damage,
                   crit_chance, crit_multiplier,
                   attack_name='single_attack_setup',
                   attack_setup=weapon_setups['single_attack_setup']
                   )

    @classmethod
    def generate_random(cls, etype='Weapon', equipable_slot='Main Hand', value=0, max_durability=10, strength=0,
                        dexterity=0, intelligence=0,
                        max_hp=0, defense=0, att_dmg_min=1, att_dmg_max=2, damage=0,
                        crit_chance=0, crit_multiplier=0,
                        attack_name='single_attack_setup',
                        attack_setup=weapon_setups['single_attack_setup']):
        quality = random.choices(sList, weights=sWeights, k=1)[0]
        quality_val = sValue.get(quality)
        equipable_slot = random.choice(['Main Hand', 'Off Hand'])
        att_dmg_min *= quality_val
        att_dmg_max = (1 + random.randint(1, 3)) * quality_val
        attack_name = random.choice(list(weapon_setups))
        attack_setup = weapon_setups[attack_name]

        return cls(quality, quality_val, etype, equipable_slot, value,
                   max_durability, strength, dexterity, intelligence,
                   max_hp, defense, att_dmg_min, att_dmg_max, damage,
                   crit_chance, crit_multiplier,
                   attack_name, attack_setup)

    def show_stats(self):
        name = f'{self.quality} {self.type}'
        slot = f'{self.equipable_slot.title():>9}'
        dmg = f'{self.att_dmg_min:>3}-{self.att_dmg_max:<3}'
        line2_left = f'Dur: {self.durability:>2}/{self.max_durability:<2} '
        line2_right = f'Damage: {dmg}'
        return f'{name:<15}{slot:>15}\n{line2_left:<15}{line2_right:>15}\n'


class Armor(Equipment):
    def __init__(self, quality='Common', quality_val=1, etype='Armor', equipable_slot='Chest', value=0,
                 max_durability=10, strength=0, dexterity=0, intelligence=0,
                 max_hp=0, defense=1, att_dmg_min=0, att_dmg_max=0, damage=0,
                 crit_chance=0, crit_multiplier=0):
        super(Armor, self).__init__(quality, quality_val, etype, equipable_slot, value,
                                    max_durability, strength, dexterity, intelligence,
                                    max_hp, defense, att_dmg_min, att_dmg_max, damage,
                                    crit_chance, crit_multiplier)

    @classmethod
    def generate(cls, quality='Common', quality_val=1, etype='Armor', equipable_slot='Chest', value=0,
                 max_durability=10, strength=0, dexterity=0, intelligence=0, max_hp=0, defense=1,
                 att_dmg_min=0, att_dmg_max=0, damage=0, crit_chance=0, crit_multiplier=0):
        return cls(quality, quality_val, etype, equipable_slot, value,
                   max_durability, strength, dexterity, intelligence,
                   max_hp, defense, att_dmg_min, att_dmg_max, damage,
                   crit_chance, crit_multiplier)

    @classmethod
    def generate_random(cls, etype='Armor', equipable_slot='Chest', value=0, max_durability=10,
                        strength=0, dexterity=0, intelligence=0, max_hp=0, defense=1,
                        att_dmg_min=0, att_dmg_max=0, damage=0, crit_chance=0, crit_multiplier=0):
        quality = random.choices(sList, weights=sWeights, k=1)[0]
        quality_val = sValue.get(quality)
        equipable_slot = random.choice(['Head', 'Chest', 'Legs', 'Feet'])
        defense = (1 + random.randint(1, 4)) * quality_val

        return cls(quality, quality_val, etype, equipable_slot, value,
                   max_durability, strength, dexterity, intelligence,
                   max_hp, defense, att_dmg_min, att_dmg_max, damage,
                   crit_chance, crit_multiplier)

    def show_stats(self):
        name = f'{self.quality} {self.type}'
        slot = f'{self.equipable_slot.title():>9}'
        line2_left = f'Dur: {self.durability:>2}/{self.max_durability:<2} '
        line2_right = f'Defense: {self.defense}'
        return f'{name:<17}{slot:>13}\n{line2_left:<15}{line2_right:>15}\n'


class Jewelry(Equipment):
    def __init__(self, quality='Common', quality_val=1, etype='Jewelry', equipable_slot='Ring', value=50,
                 strength=0, dexterity=0, intelligence=0, max_hp=0, defense=0,
                 att_dmg_min=0, att_dmg_max=0, damage=0, crit_chance=0, crit_multiplier=0):
        super(Jewelry, self).__init__(quality, quality_val, etype, equipable_slot, value,
                                      strength, dexterity, intelligence, max_hp, defense,
                                      att_dmg_min, att_dmg_max, damage, crit_chance, crit_multiplier)

    @classmethod
    def generate(cls, quality='Common', quality_val=1, etype='Jewelry', equipable_slot='Ring', value=0,
                 max_durability=10, strength=0, dexterity=0, intelligence=0, max_hp=0, defense=1,
                 att_dmg_min=0, att_dmg_max=0, damage=0, crit_chance=0, crit_multiplier=0):
        return cls(quality, quality_val, etype, equipable_slot, value,
                   strength, dexterity, intelligence,
                   max_hp, defense, att_dmg_min, att_dmg_max, damage,
                   crit_chance, crit_multiplier)

    @classmethod
    def generate_random(cls, etype='Armor', equipable_slot='Chest', value=0, max_durability=10,
                        strength=0, dexterity=0, intelligence=0, max_hp=0, defense=1,
                        att_dmg_min=0, att_dmg_max=0, damage=0, crit_chance=0, crit_multiplier=0):
        quality = random.choices(sList, weights=sWeights, k=1)[0]
        quality_val = sValue.get(quality)
        equipable_slot = random.choice(['Head', 'Chest', 'Legs', 'Feet'])
        defense = (1 + random.randint(0, 2)) * quality_val

        return cls(quality, quality_val, etype, equipable_slot, value,
                   strength, dexterity, intelligence, max_hp, defense,
                   att_dmg_min, att_dmg_max, damage, crit_chance, crit_multiplier)

    def show_stats(self):
        name = f'{self.quality} {self.type}'
        slot = f'{self.equipable_slot.title():>9}'
        line2_left = f'Dur: {self.durability:>2}/{self.max_durability:<2} '
        line2_right = f'Defense: {self.defense}'
        return f'{name:<17}{slot:>13}\n{line2_left:<15}{line2_right:>15}\n'


def create_random_item(class_type=1):
    """Generates an instance of the selected class"""
    if class_type == 1:
        item_variable = Weapon.generate_random()
        return item_variable

    elif class_type == 2:
        item_variable = Armor.generate_random()
        return item_variable

    elif class_type == 3:
        item_variable = Jewelry.generate_random()
        return item_variable


def create_random_equipable_item(how_many=1, etype=random.randint(1, 2)):
    for i in range(0, how_many):
        x = create_random_item(etype)
        return x
