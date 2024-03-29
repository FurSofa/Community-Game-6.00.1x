new_npc_stats = {
    'base_stats': {
        'vit': 4,
        'dex': 4,
        'str': 4,
        'int': 4,
        'agility': 8,
        'toughness': 9,
    },
    'stats': {
        'max_hp': 'from vit',  # vit*hp_per_vit + lvl*hp_per_lvl
        'max_mana': 'from int?',
        'armor': 'from str and toughness',
        'magic_resistance': 'from toughness',  #  and int?
        'speed': 'from dex and agility',
        'dodge': 'from dex and speed',
        'crit_chance': 'from dex',
        'crit_dmg': 'from dex',
    },
    'storage': {
        'equipped items': 'armor, weapons, ...',
        'spell book': 'spells / abilities',
        'potions': '',  # in party?
        'party': 'party instance'
    },
    'tracked_values': {
        'ct': 1000,  # when c reaches this, unit gets a turn
        'c': 0,  # holds current charge value - +speed each clock tick in battle
        'status_effects': [],
        'elemental_resistance': 0,  # from items (and toughness?)
        'hp': '',
        'mana': '',
    }
}
