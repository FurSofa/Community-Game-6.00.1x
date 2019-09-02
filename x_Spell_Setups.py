
base_spell = {
    'name': 'base_spell',
    'mana_cost': 5,
    'cool_down': 2,
    'attack_setup': {
        'target_num': 1,
        'primary': True,
        'primary_percent': 100,
        'rnd_target': True,
        'splash_dmg': 0,
        'elemental': 'physical',
        'vamp': 0,
        'can_crit': True,
        'dmg_base': 'int_based',
        'wpn_dmg_perc': 100,
        'max_hp_perc_dmg': 0,
        'c_hp_perc_dmg': 0,
        'can_dodge': True,
    },
    'cd_timer': 0,
}

heal = {
    'name': 'heal',
    'mana_cost': 5,
    'cool_down': 2,
    'attack_setup': {
        'target_num': 1,
        'primary': True,
        'primary_percent': 100,
        'rnd_target': True,
        'splash_dmg': 0,
        'elemental': 'heal',
        'vamp': 0,
        'can_crit': True,
        'dmg_base': 'int_based',
        'wpn_dmg_perc': 100,
        'max_hp_perc_dmg': 0,
        'c_hp_perc_dmg': 0,
        'can_dodge': False,
    },
    'cd_timer': 0,
}
