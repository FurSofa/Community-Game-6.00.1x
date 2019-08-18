weapon_setups = {
    'single_attack_setup': {
        'target_num': 1,
        'splash_dmg': 0,
        'primary': True,
        'primary_percent': 100,
        'rnd_target': True,
        'dmg_base': 'magic',
        'can_crit': True,
        'vamp': 0,
        'elemental': 'physical'
    },

    'multi_attack_setup': {
        'target_num': 'all',
        'splash_dmg': 50,
        'primary': False,
        'primary_percent': 100,
        'rnd_target': True,
        'dmg_base': 'physical',
        'can_crit': True,
        'vamp': 0,
        'elemental': 'physical'
    },

    'multi_attack_setup_prim_true': {
        'target_num': 2,
        'splash_dmg': 10,
        'primary': True,
        'primary_percent': 100,
        'rnd_target': True,
        'dmg_base': 'true',
        'vamp': 0,
        'can_crit': True,
        'elemental': 'true'
    },

    'single_attack_vamp': {
        'target_num': 1,
        'splash_dmg': 0,
        'primary': True,
        'primary_percent': 100,
        'rnd_target': True,
        'dmg_base': 'magic',
        'can_crit': True,
        'vamp': 25,
        'elemental': 'physical'
    },


}
basic_heal = {
    'target_num': 1,
    'splash_dmg': 0,
    'primary': True,
    'primary_percent': 100,
    'rnd_target': True,
    'dmg_base': 'magic',
    'is_heal': True
}

basic_vamp = {
    'target_num': 1,
    'splash_dmg': 0,
    'primary': True,
    'primary_percent': 100,
    'rnd_target': True,
    'dmg_base': 'magic',
    'vamp': 100
}
basic_self_vamp =  {
    'target_num': 1,
    'splash_dmg': 0,
    'primary': True,
    'primary_percent': 100,
    'rnd_target': True,
    'dmg_base': 'magic',
    'elemental': 'fire',
    'vamp': -100,
}

single = {
    'target_num': 1,
    'splash_dmg': 0,
    'primary': True,
    'primary_percent': 100,
    'rnd_target': True,
    'dmg_base': 'magic',
    'can_crit': True,
    'vamp': 0,
    'elemental': 'fire'
}

half_maxhp = {
    'target_num': 1,
    'splash_dmg': 0,
    'primary': True,
    'primary_percent': 100,
    'rnd_target': True,
    'dmg_base': 'magic',
    'can_crit': True,
    'vamp': 0,
    'elemental': 'physical',
    'wpn_dmg_perc': 0,
    'max_hp_perc_dmg': 50,
}

full_setup = {
    'target_num': 1,
    'primary': True,
    'primary_percent': 100,
    'rnd_target': True,
    'splash_dmg': 0,
    'elemental': 'physical',
    'vamp': 0,
    'can_crit': True,
    'dmg_base': 'magic',
    'wpn_dmg_perc': 100,
    'max_hp_perc_dmg': 0,
    'c_hp_perc_dmg': 0,
}

chp_vamp = {
    'target_num': 1,
    'primary': True,
    'primary_percent': 100,
    'rnd_target': True,
    'splash_dmg': 0,
    'elemental': 'physical',
    'vamp': 0,
    'can_crit': True,
    'dmg_base': 'magic',
    'wpn_dmg_perc': 100,
    'max_hp_perc_dmg': 0,
    'c_hp_perc_dmg': 0,
}

all_enemies = {'target_num': 'all',
               'splash_dmg': 50,
               'primary': False,
               'primary_percent': 100,
               'rnd_target': True,
               'dmg_base': 'physical'
               }
