import random
import json
from x_Attack_Setups import *
import x_Spell_Setups
from Item_Bases import *
import battle
from types import SimpleNamespace

test_weapon = {
            'base_stats': {
                'vit': 1,
                'dex': 2,
                'str': 0,
                'int': 0,
                'agility': 1,
                'toughness': 1,
            },
            'stats': {
                'max_hp': 13,
                'max_mana': 10,
                'armor': 0,
                'magic_resistance': 0,
                'speed': 0,
                'dodge': 0,
                'crit_chance': 2,
                'crit_dmg': 20,
                'elemental_resistance': 10,
                'wpn_dmg': 5,
            },
            'attack_name': 'single_attack_setup',
            'attack_setup': weapon_setups['single_attack_setup'],
        }


class NPC:

    def __init__(self, name='Mr. Lazy', profession='warrior', level=1, weapon=test_weapon):
        """
        Create new person """

        self.hero = False
        self.name = name
        self.profession = profession
        self.party = None  # Only one party at a time

        self.level = level
        self.xp = 0
        self.next_level = 20
        self.worth_xp = 5

        self.base_stats = {
                            'vit': 1,
                            'dex': 1,
                            'str': 1,
                            'int': 1,
                            'agility': 1,
                            'toughness': 1,
                        }

        # rewrite base stats for class_type from setup file
        with open('char_creation_setup.json', 'r') as f:
            class_stats = json.load(f)['cl_base_stats']['classes']
            if self.profession.lower() == 'warrior':
                class_key = 'str_class'
            elif self.profession.lower() == 'mage':
                class_key = 'int_class'
            else:
                class_key = 'dex_class'
            for stat in class_stats[class_key].keys():
                if stat[-6:] == '_start':
                    self.base_stats[stat[:-6]] = class_stats[class_key][stat]

        # self.stats = {
        #     # 'vit': self.base_stats.get('vit'),
        #     # 'dex': self.base_stats.get('dex'),
        #     # 'str': self.base_stats.get('str'),
        #     # 'int': self.base_stats.get('int'),
        #     # 'agility': self.base_stats.get('agility'),
        #     # 'toughness': self.base_stats.get('toughness'),
        #
        #     'max_hp': 0,
        #     'max_mana': 0,
        #     'armor': 0,
        #     'magic_resistance': 0,
        #     'speed': 0,
        #     'dodge': 0,
        #     'crit_chance': 0,
        #     'crit_dmg': 0,
        #     'elemental_resistance': 0,  # from items (and toughness?)
        #     'wpn_dmg': 0
        # }

        self.spell_book = [x_Spell_Setups.heal.copy(), x_Spell_Setups.base_spell.copy()]

        self.equip_slots = {'Main Hand': Weapon.generate(quality='Common', quality_val=1, etype='Weapon',
                                                         equipable_slot='Main Hand',
                                                         att_dmg_min=1, att_dmg_max=3),
                            'Off Hand': None,
                            'Head': None,
                            'Chest': None,
                            'Legs': None,
                            'Feet': None,
                            'Ring': None,
                            'Necklace': None,
                            }

        level_up_counter = 1
        while level_up_counter < level:
            self.level_up()
            level_up_counter += 1

        # self.calculate_stats_with_equipment()

        self.tracked_values = {
                                'ct': 1000,  # when c reaches this, unit gets a turn
                                'c': 0,  # holds current charge value - +speed each clock tick in battle
                                'status_effects': [],

                                'hp': self.max_hp,
                                'mana': self.max_mana,
                            }

    # def combine_base_stats_with_equipment(self):
    #     # base_stats = {
    #     #     'str': self.base_stats['str'],
    #     #     'dex': self.base_stats['dex'],
    #     #     'int': self.base_stats['int'],
    #     #     'vit': self.base_stats['vit'],
    #     #     'agility': self.base_stats['agility'],
    #     #     'toughness': self.base_stats['toughness'],
    #     # }
    #     #
    #     gear = [value for value in self.equip_slots.values() if value]
    #     for key in self.base_stats.keys():
    #         self.stats[key] = self.base_stats[key] + sum([item.base_stats.get(key, 0) for item in gear])

    def get_conversion_ratios(self):
        with open('char_creation_setup.json', 'r') as f:
            conversion_ratios = json.load(f)['conversion_ratios']
        return conversion_ratios

    def get_stat_from_equipment(self, stat, base_stat=True ):
        gear = self.get_equipped_items()
        # gear = [value for value in self.equip_slots.values() if value]
        if base_stat:
            return sum([item.base_stats.get(stat, 0) for item in gear])
        else:
            return sum([item.stats.get(stat, 0) for item in gear])

    # full_ values are for display only
    @property
    def full_vit(self):
        stat = 'vit'
        return self.base_stats[stat] + self.get_stat_from_equipment(stat)

    @property
    def full_dex(self):
        stat = 'dex'
        return self.base_stats[stat] + self.get_stat_from_equipment(stat)

    @property
    def full_str(self):
        stat = 'str'
        return self.base_stats[stat] + self.get_stat_from_equipment(stat)

    @property
    def full_int(self):
        stat = 'int'
        return self.base_stats[stat] + self.get_stat_from_equipment(stat)

    @property
    def full_agility(self):
        stat = 'agility'
        return self.base_stats[stat] + self.get_stat_from_equipment(stat)

    @property
    def full_toughness(self):
        stat = 'toughness'
        return self.base_stats[stat] + self.get_stat_from_equipment(stat)

    @property
    def vit(self):
        return self.full_vit

    @property
    def dex(self):
        return self.full_dex

    @property
    def str(self):
        return self.full_str

    @property
    def int(self):
        return self.full_int

    @property
    def agility(self):
        return self.full_agility

    @property
    def toughness(self):
        return self.full_toughness


# deriving stats
    #  full values are for display only


    @property
    def full_speed(self):
        stat = 'speed'
        conversion_ratios = self.get_conversion_ratios()
        speed_per_dex = conversion_ratios['dex_to_speed']['speed_per_dex']
        speed_per_agility = conversion_ratios['dex_to_speed']['speed_per_agility']
        speed_factor = conversion_ratios['dex_to_speed']['speed_factor']
        speed_start = conversion_ratios['dex_to_speed']['speed_start']

        speed_from_dex = self.dex * speed_per_dex
        speed_from_agility = self.agility * speed_per_agility
        speed = (speed_from_dex + speed_from_agility) * speed_factor + speed_start
        return speed + self.get_stat_from_equipment(stat, base_stat=False)

    @property
    def full_max_hp(self):
        stat = 'max_hp'
        conversion_ratios = self.get_conversion_ratios()
        hp_start = conversion_ratios['vit_to_hp']['start']
        hp_per_vit = conversion_ratios['vit_to_hp']['hp_per_vit']
        hp_per_lvl = conversion_ratios['vit_to_hp']['hp_per_lvl']
        max_hp = self.vit * hp_per_vit + self.level * hp_per_lvl + hp_start
        return max_hp + self.get_stat_from_equipment(stat, base_stat=False)

    @property
    def full_crit_chance(self):
        stat = 'crit_chance'
        conversion_ratios = self.get_conversion_ratios()
        crit_chance_start = conversion_ratios['dex_to_crit']['chance_start']
        crit_chan_per_level = conversion_ratios['dex_to_crit']['crit_chan_per_level']
        crit_chan_per_dex = conversion_ratios['dex_to_crit']['crit_chan_per_dex']

        crit_chance_from_dex = self.dex * crit_chan_per_dex
        crit_chance_from_lvl = self.level * crit_chan_per_level
        crit_chance = crit_chance_from_dex + crit_chance_from_lvl + crit_chance_start
        return crit_chance + self.get_stat_from_equipment(stat, base_stat=False)

    @property
    def full_crit_dmg(self):
        stat = 'crit_dmg'
        conversion_ratios = self.get_conversion_ratios()
        crit_dmg_start = conversion_ratios['dex_to_crit']['dmg_start']
        crit_dmg_per_level = conversion_ratios['dex_to_crit']['crit_dmg_per_level']
        crit_dmg_per_dex = conversion_ratios['dex_to_crit']['crit_dmg_per_dex']

        crit_dmg_from_dex = self.dex * crit_dmg_per_dex
        crit_dmg_from_level = self.level * crit_dmg_per_level
        crit_dmg = crit_dmg_from_dex + crit_dmg_from_level + crit_dmg_start
        return crit_dmg + self.get_stat_from_equipment(stat, base_stat=False)

    @property
    def full_dodge(self):
        stat = 'dodge'
        conversion_ratios = self.get_conversion_ratios()
        dodge_start = conversion_ratios['dex_speed_to_dodge']['start']
        dodge_per_speed = conversion_ratios['dex_speed_to_dodge']['dodge_per_speed']
        dodge_per_dex = conversion_ratios['dex_speed_to_dodge']['dodge_per_dex']

        dodge_from_dex = self.dex * dodge_per_dex
        dodge_from_speed = self.speed * dodge_per_speed
        dodge = dodge_from_dex + dodge_from_speed + dodge_start
        return dodge + self.get_stat_from_equipment(stat, base_stat=False)

    @property
    def full_armor(self):
        stat = 'armor'
        conversion_ratios = self.get_conversion_ratios()
        armor_per_str = conversion_ratios['str_to_armor']['armor_per_str']
        armor_per_lvl = conversion_ratios['str_to_armor']['armor_per_level']
        armor_per_toughness = conversion_ratios['toughness_to_armor']['armor_per_toughness']

        armor_from_str = (self.str * armor_per_str) + (self.level * armor_per_lvl)
        armor_from_toughness = self.toughness * armor_per_toughness
        armor = armor_from_str + armor_from_toughness
        return armor + self.get_stat_from_equipment(stat, base_stat=False)

    # TODO: find a formula for max mana
    @property
    def full_max_mana(self):
        stat = 'max_mana'
        return (20 + 5 * self.level) + self.get_stat_from_equipment(stat, base_stat=False)

    # TODO: find a formula for mana regen
    @property
    def full_mana_regen(self):
        stat = 'mana_regen'
        return 2 + self.get_stat_from_equipment(stat, base_stat=False)

    @property
    def full_elemental_resistance(self):
        stat = 'elemental_resistance'
        return self.get_stat_from_equipment(stat, base_stat=False)

    @property
    def full_magic_resistance(self):
        stat = 'magic_resistance'
        return self.get_stat_from_equipment(stat, base_stat=False)

    @property
    def full_wpn_dmg(self):
        stat = 'wpn_dmg'
        return self.get_stat_from_equipment(stat, base_stat=False)

    # derived stats to use
    #  TODO: add modifiers for status effects here
    @property
    def speed(self):
        return self.full_speed

    @property
    def dodge(self):
        return self.full_dodge

    @property
    def max_hp(self):
        return self.full_max_hp

    @property
    def crit_chance(self):
        return self.full_crit_chance

    @property
    def crit_dmg(self):
        return self.full_crit_dmg

    @property
    def max_mana(self):
        return self.full_max_mana

    @property
    def mana_regen(self):
        return self.full_mana_regen

    @property
    def armor(self):
        return self.full_armor

    @property
    def wpn_dmg(self):
        return self.full_wpn_dmg

    @property
    def elemental_resistance(self):
        return self.full_elemental_resistance

    @property
    def magic_resistance(self):
        return self.full_magic_resistance

    @property
    def hp(self):
        return self.tracked_values['hp']

    @property
    def mana(self):
        return self.tracked_values['mana']

    @property
    def attack_dmg(self):
        dmg_base = self.equip_slots['Main Hand'].attack_setup['dmg_base']
        dummy_target = SimpleNamespace(hp=1, max_hp=1)
        # TODO: get dot notation for the dummy going
        return battle.generate_dmg(self, dummy_target, dmg_base=dmg_base)

    # def derive_stats(self):
    #     with open('char_creation_setup.json', 'r') as f:
    #         conversion_ratios = json.load(f)['conversion_ratios']
    #
    #     #  armor
    #     # armor_per_str = 2
    #     # armor_per_lvl = 2
    #     # armor_per_toughness = 4
    #
    #     armor_per_str = conversion_ratios['str_to_armor']['armor_per_str']
    #     armor_per_lvl = conversion_ratios['str_to_armor']['armor_per_level']
    #     armor_per_toughness = conversion_ratios['toughness_to_armor']['armor_per_toughness']
    #
    #     #  speed
    #     # speed_per_dex = 0.03
    #     # speed_per_agility = 0.2
    #     # speed_factor = 0.1
    #     # speed_start = 9
    #
    #     speed_per_dex = conversion_ratios['dex_to_speed']['speed_per_dex']
    #     speed_per_agility = conversion_ratios['dex_to_speed']['speed_per_agility']
    #     speed_factor = conversion_ratios['dex_to_speed']['speed_factor']
    #     speed_start = conversion_ratios['dex_to_speed']['speed_start']
    #
    #     #  dodge
    #     dodge_start = 3
    #     dodge_per_speed = 0.3
    #     dodge_per_dex = 0.2
    #
    #     dodge_start = conversion_ratios['dex_speed_to_dodge']['start']
    #     dodge_per_speed = conversion_ratios['dex_speed_to_dodge']['dodge_per_speed']
    #     dodge_per_dex = conversion_ratios['dex_speed_to_dodge']['dodge_per_dex']
    #
    #     #  crit
    #     # crit_chance_start = 5
    #     # crit_chan_per_level = 0.25
    #     # crit_chan_per_dex = 0.25
    #     #
    #     # crit_dmg_start = 125
    #     # crit_dmg_per_level = 1
    #     # crit_dmg_per_dex = 3
    #
    #     crit_chance_start = conversion_ratios['dex_to_crit']['chance_start']
    #     crit_chan_per_level = conversion_ratios['dex_to_crit']['crit_chan_per_level']
    #     crit_chan_per_dex =conversion_ratios['dex_to_crit']['crit_chan_per_dex']
    #
    #     crit_dmg_start = conversion_ratios['dex_to_crit']['dmg_start']
    #     crit_dmg_per_level = conversion_ratios['dex_to_crit']['crit_dmg_per_level']
    #     crit_dmg_per_dex = conversion_ratios['dex_to_crit']['crit_dmg_per_dex']
    #
    #     #  hp
    #     # hp_start = 800
    #     # hp_per_vit = 40
    #     # hp_per_lvl = 15
    #
    #     hp_start = conversion_ratios['vit_to_hp']['start']
    #     hp_per_vit = conversion_ratios['vit_to_hp']['hp_per_vit']
    #     hp_per_lvl = conversion_ratios['vit_to_hp']['hp_per_lvl']
    #
    #     # speed calculation
    #     speed_from_dex = self.stats['dex'] * speed_per_dex
    #     speed_from_agility = self.stats['agility'] * speed_per_agility
    #     self.stats['speed'] = (speed_from_dex + speed_from_agility) * speed_factor + speed_start
    #
    #     #  dodge calculation
    #     dodge_from_dex = self.stats['dex'] * dodge_per_dex
    #     dodge_from_speed = self.stats['speed'] * dodge_per_speed
    #     self.stats['dodge'] = dodge_from_dex + dodge_from_speed + dodge_start
    #
    #     #  armor calculation
    #     armor_from_str = (self.stats['str'] * armor_per_str) + (self.level * armor_per_lvl)
    #     armor_from_toughness = self.stats['toughness'] * armor_per_toughness
    #     self.stats['armor'] = armor_from_str + armor_from_toughness
    #
    #     #  crit calculation
    #     crit_chance_from_dex = self.stats['dex'] * crit_chan_per_dex
    #     crit_chance_from_lvl = self.level * crit_chan_per_level
    #     self.stats['crit_chance'] = crit_chance_from_dex + crit_chance_from_lvl + crit_chance_start
    #
    #     crit_dmg_from_dex = self.stats['dex'] * crit_dmg_per_dex
    #     crit_dmg_from_level = self.level * crit_dmg_per_level
    #     self.stats['crit_dmg'] = crit_dmg_from_dex + crit_dmg_from_level + crit_dmg_start
    #
    #     #  hp calculation
    #     self.stats['max_hp'] = self.stats['vit'] * hp_per_vit + self.level * hp_per_lvl + hp_start
    #
    # def combine_derived_stats_with_equipment(self):
    #     keys_to_combine = ['max_hp', 'max_mana', 'armor', 'magic_resistance', 'speed', 'dodge',
    #                        'crit_chance', 'crit_dmg', 'elemental_resistance', 'wpn_dmg']
    #     gear = [value for value in self.equip_slots.values() if value]
    #     for key in keys_to_combine:
    #         self.stats[key] = self.stats[key] + sum([item.stats.get(key, 0) for item in gear])
    #
    # def calculate_stats_with_equipment(self):
    #     self.combine_base_stats_with_equipment()
    #     self.derive_stats()
    #     self.combine_derived_stats_with_equipment()

    def stat_growth(self):
        with open('char_creation_setup.json', 'r') as f:
            class_stats = json.load(f)['cl_base_stats']['classes']
        if self.profession.lower() == 'warrior':
            class_key = 'str_class'
        elif self.profession.lower() == 'mage':
            class_key = 'int_class'
        else:
            class_key = 'dex_class'

        for stat in class_stats[class_key].keys():
            if stat[-6:] == '_p_lvl':
                self.base_stats[stat[:-6]] += class_stats[class_key][stat]

    def level_up(self):
        self.level += 1
        self.xp -= self.next_level
        self.next_level = round(4 * (self.level ** 3) / 5) + 20
        print(f'{self.name} is now {self.level}!')
        self.stat_growth()
        # self.calculate_stats_with_equipment()
        self.tracked_values['hp'] = self.stats['max_hp']
        self.tracked_values['mana'] = self.stats['max_mana']

    @property
    def is_alive(self) -> bool:
        return self.tracked_values['hp'] > 0

    def set_hp(self, amount):
        """
        set the hp safely
        :param amount: int: to change / can be positive or negative
        :return: amount
        """
        self.tracked_values['hp'] = min(self.tracked_values['hp'] + amount, self.max_hp)
        if self.tracked_values['hp'] < 0:
            self.tracked_values['hp'] = 0

    def set_mana(self, amount):
        """
        set the mana safely
        :param amount: int: to change / can be positive or negative
        :return: amount
        """
        self.tracked_values['mana'] = min(self.tracked_values['mana'] + amount, self.max_mana)
        if self.tracked_values['mana'] < 0:
            self.tracked_values['mana'] = 0

    def choose_target(self, target_party):
        """
        picks random target from target_party.members
        :param target_party: party instance
        :return: person from party
        """
        if len(target_party) > 1:
            if self.party.has_hero() or self.party.game.difficulty == 'Medium':
                choice = random.randrange(len(target_party))
                target = target_party[choice]
            else:
                if self.party.game.difficulty == 'Hard':
                    target = min(target_party, key=lambda member: member.tracked_values['hp'])
                elif self.party.game.difficulty == 'Easy':
                    target = max(target_party, key=lambda member: member.tracked_values['hp'])
        else:
            target = target_party[0]
        return target

    def choose_attack(self, attack_options):
        choice = random.choice([i for i in range(len(attack_options))])
        return choice

    def choose_battle_action(self, possible_actions):
        """
        ENDPOINT for battle
        npc will always choose basic attack
        :param possible_actions:
        :return: -
        """
        # TODO: add logic to choose spells
        possible_actions = ['attack', ]
        if self.party.game.difficulty == 'Medium':
            heal_under = 0.2
        elif self.party.game.difficulty == 'Hard':
            heal_under = 0.3
        else:
            heal_under = 0.05

        # if self.hp / self.max_hp < heal_under:
        #     possible_actions.append('heal')
        action = random.choice(possible_actions)
        return action

    def show_gear(self):
        items = [self.equip_slots['Main Hand'],
                 self.equip_slots['Off Hand'],
                 self.equip_slots['Head'],
                 self.equip_slots['Chest'],
                 self.equip_slots['Legs'],
                 self.equip_slots['Feet'],
                 self.equip_slots['Ring'],
                 self.equip_slots['Necklace']]
        gear = [item for item in items if item]
        for i in gear:
            print(i.item)

    def get_equipped_items(self):
        """
        :return: list of currently equipped items
        """
        return [value for value in self.equip_slots.values() if value]

    def add_xp(self, xp):
        self.xp += xp
        print(f'{self.name} gained {xp} xp!')
        if self.xp > self.next_level:
            self.level_up()


    def info_card(self):

        name = f'{self.name}'
        prof = f'{self.profession}'

        hp = f'HP: {self.hp:>3}/{self.max_hp:<3}'  # 10
        defense = f'Def: {self.armor}'  # 8

        lvl = f'Lvl: {self.level}'
        xp = f'XP: {self.xp}/{self.next_level}'

        stats_str = f'Str: {self.str}'  # Trying 3 probly 2
        stats_dex = f'Dex: {self.dex}'
        stats_int = f'Int: {self.int}'

        dmg_w = 'DMG: '
        dmg_stat = f'{self.wpn_dmg}/{self.attack_dmg}'  # 11  # TODO: get calculated dmg?
        crit_w = f'Crit %: '
        crit_stat = f'{self.crit_chance:>2}/{self.crit_dmg:<3}'  # 15

        # Combine L an R lines
        name = f'{name:<1}{prof:>{21 - len(name)}}'
        level_xp = f'{lvl}{xp:>{21 - len(lvl)}}'
        hp_def = f'{hp}{defense:>{21 - len(hp)}}'
        stats = f'{stats_str:<7}{stats_dex:<7}{stats_int:<7}'
        dmg = f'{dmg_w}{dmg_stat:>{21 - len(dmg_w)}}'
        crit = f'{crit_w}{crit_stat:>{21 - len(crit_w)}}'
        return [name, level_xp, hp_def, stats, dmg, crit]

    def show_stats(self):
        print(f'\n{self.name},the {self.profession}\n'
              f'Level:\t{self.level:>4}  XP: {self.xp:>6}/{self.next_level}\n'
              f'HP:\t   {self.tracked_values["hp"]}/{self.max_hp:<4}\n'
              f'Str:\t   {self.str:<3}Damage: {self.wpn_dmg:>3}/{self.attack_dmg:<3}\n' 
              f'Dex:\t   {self.dex:<3}Crit:  {self.crit_chance}%/{self.crit_dmg}%\n'
              f'Int:\t   {self.int:<3}Defence: {self.armor:>5}\n')

    def show_combat_stats(self):
        name = f'{self.name}, the {self.profession}'
        hp = f'Hp: {self.hp:>2}/{self.max_hp:<2}'
        dmg = f'Dmg: {self.wpn_dmg:>2}/{self.attack_dmg:<2}'  # TODO: get calculated stats?
        return f'{name:^23} ' \
               f'{hp:<8} ' \
               f'{dmg:<13}'




    def __repr__(self):
        return self.name

    def __str__(self):
        return f'{self.name}, the {self.profession}'

    @classmethod
    def generate(cls, name='Jeb', profession='Warrior', level=1):
        """
        Create new character at level 1
        """
        return cls(name, profession, level)

    @classmethod
    def generate_random(cls, level=1):
        """
        Create new random character at level 1
        """
        level = level
        name = random.choice(['Lamar', 'Colin', 'Ali', 'Jackson', 'Minky',
                              'Leo', 'Phylis', 'Lindsay', 'Tongo', 'Paku', ])
        profession = random.choice(['Warrior', 'Archer', 'Mage', 'Blacksmith', 'Thief', 'Bard'])
        if name == 'Minky':
            profession = 'Miffy Muffin'
        if name == 'Colin':
            profession = 'Bard of Bass'
        return cls(name, profession, level)

