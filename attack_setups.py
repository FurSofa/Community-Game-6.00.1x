weapon_setups = {
    'single_attack_setup': {
        'target_num': 1,
        'splash_dmg': 0,
        'primary': True,
        'primary_percent': 100,
        'rnd_target': True,
        'dmg_type': 'physical',
        'is_true_dmg': False
    },

    'multi_attack_setup': {
        'target_num': 'all',
        'splash_dmg': 50,
        'primary': False,
        'primary_percent': 100,
        'rnd_target': True,
        'dmg_type': 'physical',
    },

    'multi_attack_setup_prim_true': {
        'target_num': 2,
        'splash_dmg': 10,
        'primary': True,
        'primary_percent': 100,
        'rnd_target': True,
        'dmg_type': 'magic',
    },
}
basic_heal = {
    'target_num': 1,
    'splash_dmg': 0,
    'primary': True,
    'primary_percent': 100,
    'rnd_target': True,
    'dmg_type': 'magic',
    'is_heal': True
}

basic_vamp = {
    'target_num': 1,
    'splash_dmg': 0,
    'primary': True,
    'primary_percent': 100,
    'rnd_target': True,
    'dmg_type': 'magic',
    'vamp': 100
}
basic_self_vamp =  {
    'target_num': 1,
    'splash_dmg': 0,
    'primary': True,
    'primary_percent': 100,
    'rnd_target': True,
    'dmg_type': 'magic',
    'vamp': -100
}

single = {'target_num': 1,
          'splash_dmg': 0,
          'primary': True,
          'primary_percent': 100,
          'rnd_target': True,
          'dmg_type': 'physical'
          }

all_enemies = {'target_num': 'all',
               'splash_dmg': 50,
               'primary': False,
               'primary_percent': 100,
               'rnd_target': True,
               'dmg_type': 'physical'
               }
