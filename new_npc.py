
class NPC:
    """
    access points:
    pickup_gear() to give the player a new weapon
    choose_battle_action() to start a battle turn (choosing actions and executing the appropriate methods)
    """

    def __init__(self, weapon, name='Mr. Lazy', profession='warrior', level=1):
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
                            'vit': 4,
                            'dex': 4,
                            'str': 4,
                            'int': 4,
                            'agility': 8,
                            'toughness': 9,
                        }
        # Base Stats Section!
        self.derived_stats = {
            'vit': self.base_stats.get('vit'),
            'dex': self.base_stats.get('dex'),
            'str': self.base_stats.get('str'),
            'int': self.base_stats.get('int'),
            'agility': self.base_stats.get('agility'),
            'toughness': self.base_stats.get('toughness'),

            'max_hp': 0,
            'max_mana': 0,
            'armor': 0,
            'magic_resistance': 0,
            'speed': 0,
            'dodge': 0,
            'crit_chance': 0,
            'crit_dmg': 0,
        }
        # {
        #     'max_hp': 'from vit',  # vit*hp_per_vit + lvl*hp_per_lvl
        #     'max_mana': 'from int?',
        #     'armor': 'from str and toughness',
        #     'magic_resistance': 'from toughness',  # and int?
        #     'speed': 'from dex and agility',
        #     'dodge': 'from dex and speed',
        #     'crit_chance': 'from dex',
        #     'crit_dmg': 'from dex',
        # },

        self.current_stats = {}  # calculated stats with gear

        self.tracked_values = {
                                'ct': 1000,  # when c reaches this, unit gets a turn
                                'c': 0,  # holds current charge value - +speed each clock tick in battle
                                'status_effects': [],
                                'elemental_resistance': 0,  # from items (and toughness?)
                                'hp': '',
                                'mana': '',
                            }

        self.equip_slots = {'Main Hand': weapon,  # Weapon.generate(quality='Common', quality_val=1, etype='Weapon',
        #                                                  equipable_slot='Main Hand',
        #                                                  att_dmg_min=1, att_dmg_max=3),
                            'Off Hand': None,
                            'Head': None,
                            'Chest': None,
                            'Legs': None,
                            'Feet': None,
                            'Ring': None,
                            'Necklace': None,
                            }
        # Calculate stats and gear
        # self.stat_growth()
        # self.calculate_stats()

    def combine_base_stats_with_equipment(self):
        # base_stats = {
        #     'str': self.base_stats['str'],
        #     'dex': self.base_stats['dex'],
        #     'int': self.base_stats['int'],
        #     'vit': self.base_stats['vit'],
        #     'agility': self.base_stats['agility'],
        #     'toughness': self.base_stats['toughness'],
        # }
        #
        gear = [value for value in self.equip_slots.values() if value]
        for key in self.base_stats.keys():
            self.derived_stats[key] = self.base_stats[key] + sum([item.get('base_stats')[key] for item in gear])

        pass


    def derive_stats(self):
        #  armor
        armor_per_str = 2
        armor_per_lvl = 2
        armor_per_toughness = 4

        #  speed
        speed_per_dex = 0.03
        speed_per_agility = 0.2
        speed_factor = 0.1
        speed_start = 9

        #  dodge
        dodge_start = 3
        dodge_per_speed = 0.3
        dodge_per_dex = 0.2

        #  crit
        crit_chance_start = 5
        crit_chan_per_level = 0.25
        crit_chan_per_dex = 0.25

        crit_dmg_start = 125
        crit_dmg_per_level = 1
        crit_dmg_per_dex = 3

        #  hp
        hp_start = 800
        hp_per_vit = 40
        hp_per_lvl = 15

        # speed calculation
        speed_from_dex = self.derived_stats['dex'] * speed_per_dex
        speed_from_agility = self.derived_stats['agility'] * speed_per_agility
        self.derived_stats['speed'] = (speed_from_dex + speed_from_agility) * speed_factor + speed_start

        #  dodge calculation
        dodge_from_dex = self.derived_stats['dex'] * dodge_per_dex
        dodge_from_speed = self.derived_stats['speed'] * dodge_per_speed
        self.derived_stats['dodge'] = dodge_from_dex + dodge_from_speed + dodge_start

        #  armor calculation
        armor_from_str = (self.derived_stats['str'] * armor_per_str) + (self.level * armor_per_lvl)
        armor_from_toughness = self.derived_stats['toughness'] * armor_per_toughness
        self.derived_stats['armor'] = armor_from_str + armor_from_toughness

        #  crit calculation
        crit_chance_from_dex = self.derived_stats['dex'] * crit_chan_per_dex
        crit_chance_from_lvl = self.level * crit_chan_per_level
        self.derived_stats['crit_chance'] = crit_chance_from_dex + crit_chance_from_lvl + crit_chance_start

        crit_dmg_from_dex = self.derived_stats['dex'] * crit_dmg_per_dex
        crit_dmg_from_level = self.level * crit_dmg_per_level
        self.derived_stats['crit_dmg'] = crit_dmg_from_dex + crit_dmg_from_level + crit_dmg_start

        #  hp calculation
        self.derived_stats['max_hp'] = self.derived_stats['vit'] * hp_per_vit + self.level * hp_per_lvl + hp_start


    def combine_derived_stats_with_equipment(self):
        keys_to_combine = ['max_hp', 'max_mana', 'armor', 'magic_resistance', 'speed', 'dodge', 'crit_chance', 'crit_dmg']
        gear = [value for value in self.equip_slots.values() if value]
        for key in keys_to_combine:
            self.derived_stats[key] = self.derived_stats[key] + sum([item.get('derived_stats')[key] for item in gear])

    def calculate_stats_with_equipment(self):
        self.combine_base_stats_with_equipment()
        self.derive_stats()
        self.combine_derived_stats_with_equipment()


test_weapon = {
    'base_stats': {
                'vit': 2,
                'dex': 1,
                'str': 0,
                'int': 0,
                'agility': 1,
                'toughness': 3,
    },
    'derived_stats': {
            'max_hp': 11,
            'max_mana': 3,
            'armor': 33,
            'magic_resistance': 0,
            'speed': 2,
            'dodge': 1,
            'crit_chance': 50,
            'crit_dmg': 100,
        },
}
