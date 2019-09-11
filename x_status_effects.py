dex_buff = {
    'name': '+10 percent dex',
    'msg': 'raises his power level',
    'pct_dex': 10,
    'flat_dex': 1,
    'ticks': 2,
    'caster': None,
    'attack_setup': None,
}

bleed = {
    'name': 'bleed',
    'msg': 'is bleeding all over the flor',
    'ticks': 4,
    'caster': None,
    'attack_setup': {
        'target_num': 1,
        'max_hp_pct_dmg': 3,
        'can_dodge': False,
        'dmg_base': 'dex_based',
        'wpn_dmg_pct': 0,
    }
}
