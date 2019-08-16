import random
from vfx import *
import string
from Item_Bases import Equipment
from attack_setups import weapon_setups


class Spell(Equipment):
    def __init__(self, quality, quality_val=1, etype='Spell', equipable_slot='Main Hand', value=0,
                 max_durability=10, strength=0, dexterity=0, intelligence=0,
                 max_hp=0, defense=0, att_dmg_min=1, att_dmg_max=3, damage=0,
                 crit_chance=1, crit_multiplier=4,
                 attack_name='single_attack_setup',
                 attack_setup=weapon_setups['single_attack_setup']):
        super(Spell, self).__init__(quality, quality_val, etype, equipable_slot, value,
                                    max_durability, strength, dexterity, intelligence,
                                    max_hp, defense, att_dmg_min, att_dmg_max, damage,
                                    crit_chance, crit_multiplier)
        self.attack_name = attack_name
        self.attack_setup = attack_setup

    @classmethod
    def generate(cls, quality='Common', quality_val=1, etype='Spell', equipable_slot='Main Hand', value=0,
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
    def generate_random(cls, etype='Spell', equipable_slot='Main Hand', value=0, max_durability=10, strength=0,
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
