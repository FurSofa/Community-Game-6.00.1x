import random
from helper_functions import select_from_list


def deal_multi_dmg(attacker, target_party, target_num='all', splash_dmg=25,
                   primary=True, primary_percent=100, rnd_target=True,
                   dmg_type='pysical'):

    if target_num == 'all' or target_num > len(target_party.members):
        target_num = len(target_party.members)

    members_list = target_party.members[:]
    dmg_received = 0

    # if primary:
    #     print('target choice:')
    #     target = attacker.choose_target(members_list)
    #     print(target.name)
    #     dmg_dealt, is_crit = attacker.calculate_dmg(dmg_type)
    #     dmg_dealt = dmg_dealt * primary_percent // 100
    #     dmg_received += target.take_dmg(dmg_dealt, dmg_type)
    #
    #     print(attacker.display(), 'deals', dmg_received, 'dmg to', target.display())
    #
    #     members_list.remove(target)
    #     target_num -= 1

    while target_num > 0:
        if primary:
            target = attacker.choose_target(members_list)
            dmg_mod = primary_percent
            primary = False
        else:
            dmg_mod = splash_dmg
            if rnd_target:
                target = random.choice(members_list)
            elif target_num < len(members_list):
                target = attacker.choose_target(members_list)
            else:
                target = members_list[0]
        dmg_dealt, is_crit = attacker.calculate_dmg(dmg_type)
        if is_crit:
            print('CRIT CRIT CRIT YAY!')
            dmg_dealt = dmg_dealt * dmg_mod // 100
            dmg_received_single = target.take_dmg(dmg_dealt, dmg_type)
        print(attacker.name, 'hits', target.name, 'for', dmg_dealt, dmg_type, 'dmg and does', dmg_received_single, 'dmg')
        dmg_received += dmg_received_single
        members_list.remove(target)
        target_num -= 1
    return dmg_received

# def attack(attacker,)
# attack = {
#     'dmg_type': ['true', 'physical', 'magic'],
#     'dmg': 'amount or range',
#     'is_crit': 'bool',  # or percentage and calc it through that
#     'crit_dmg': 'multiplicator if is_crit',
#     'target': 'person_obj',
#     'target_defense': ['physical', 'magic'],
#     'with_primary': 'bool',
#     'primary_dmg_%': 'int',
#     'num_targets': 'int',
#     'splash_dmg_%': 'int',
# }


