weapon_setups1 = {
    'single_attack_setup': {
        'target_num': 1,
        'splash_dmg': 0,
        'primary': True,
        'primary_pct': 100,
        'rnd_target': True,
        'dmg_type': 'physical',
    },

    'multi_attack_setup': {
        'target_num': 'all',
        'splash_dmg': 50,
        'primary': False,
        'primary_pct': 100,
        'rnd_target': True,
        'dmg_type': 'physical',
    },

    'multi_attack_setup_prim_true': {
        'target_num': 2,
        'splash_dmg': 10,
        'primary': True,
        'primary_pct': 100,
        'rnd_target': True,
        'dmg_type': 'magic',
    },
}

single = {'target_num': 1,
          'splash_dmg': 0,
          'primary': True,
          'primary_pct': 100,
          'rnd_target': True,
          'dmg_type': 'physical'
          }

all_enemies = {'target_num': 'all',
               'splash_dmg': 50,
               'primary': False,
               'primary_pct': 100,
               'rnd_target': True,
               'dmg_type': 'physical'
               }
weapon_setups = {
    'single_attack_setup': {
        'target_num': 1,
        'splash_dmg': 0,
        'primary': True,
        'primary_pct': 100,
        'rnd_target': True,
        'dmg_base': 'dex',
        'can_crit': True,
        'can_dodge': True,
        'vamp': 0,
        'elemental': 'physical'
    },

    'multi_attack_setup': {
        'target_num': 'all',
        'splash_dmg': 50,
        'primary': False,
        'primary_pct': 100,
        'rnd_target': True,
        'dmg_base': 'str',
        'can_crit': True,
        'vamp': 0,
        'elemental': 'physical'
    },

    'multi_attack_setup_prim_true': {
        'target_num': 2,
        'splash_dmg': 10,
        'primary': True,
        'primary_pct': 100,
        'rnd_target': True,
        'dmg_base': 'dex',
        'vamp': 0,
        'can_crit': True,
        'elemental': 'true'
    },

    'single_attack_vamp': {
        'target_num': 1,
        'splash_dmg': 0,
        'primary': True,
        'primary_pct': 100,
        'rnd_target': True,
        'dmg_base': 'int',
        'can_crit': True,
        'vamp': 25,
        'elemental': 'physical'
    },


}
basic_heal = {
    'target_num': 1,
    'splash_dmg': 0,
    'primary': True,
    'primary_pct': 100,
    'rnd_target': True,
    'dmg_base': 'magic',
    'is_heal': True
}

basic_vamp = {
    'target_num': 1,
    'splash_dmg': 0,
    'primary': True,
    'primary_pct': 100,
    'rnd_target': True,
    'dmg_base': 'magic',
    'vamp': 100
}
basic_self_vamp =  {
    'target_num': 1,
    'splash_dmg': 0,
    'primary': True,
    'primary_pct': 100,
    'rnd_target': True,
    'dmg_base': 'magic',
    'elemental': 'fire',
    'vamp': -100,
}

single = {
    'target_num': 1,
    'splash_dmg': 0,
    'primary': True,
    'primary_pct': 100,
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
    'primary_pct': 100,
    'rnd_target': True,
    'dmg_base': 'magic',
    'can_crit': True,
    'vamp': 0,
    'elemental': 'physical',
    'wpn_dmg_pct': 0,
    'max_hp_pct_dmg': 50,
}

full_setup = {
    'target_num': 1,
    'primary': True,
    'primary_pct': 100,
    'rnd_target': True,
    'splash_dmg': 0,
    'elemental': 'physical',
    'vamp': 0,
    'can_crit': True,
    'dmg_base': 'int_based',
    'wpn_dmg_pct': 100,
    'max_hp_pct_dmg': 0,
    'c_hp_pct_dmg': 0,
    'can_dodge': True,
}

chp_vamp = {
    'target_num': 1,
    'primary': True,
    'primary_pct': 100,
    'rnd_target': True,
    'splash_dmg': 0,
    'elemental': 'physical',
    'vamp': 0,
    'can_crit': True,
    'dmg_base': 'magic',
    'wpn_dmg_pct': 100,
    'max_hp_pct_dmg': 0,
    'c_hp_pct_dmg': 0,
}

all_enemies = {'target_num': 'all',
               'splash_dmg': 50,
               'primary': False,
               'primary_pct': 100,
               'rnd_target': True,
               'dmg_base': 'physical'
               }
