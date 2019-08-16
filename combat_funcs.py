import random
from attack_setups import weapon_setups


def battle_menu(attacker, enemy_party):
    action = attacker.choose_battle_action(enemy_party).lower()

    if action == 'attack':
        # TODO: make this independent of setup file! (get the setup from the weapon)
        attack_options = [item.attack_name for item in
                          [attacker.equip_slots['Main Hand'], attacker.equip_slots['Off Hand']] if item]

        setup_key = attacker.choose_attack(attack_options)
        setup = weapon_setups[setup_key]
        dmg_done = execute_attack(attacker, enemy_party, **setup)

    elif action == 'show hero stats':
        attacker.party.display_single_member_item_card(attacker)
        battle_menu(attacker, enemy_party)

    elif action == 'heal':
        attacker.heal(attacker.calculate_dmg())


def execute_attack(attacker, target_party, target_num='all', splash_dmg=25,
                   primary=True, primary_percent=100, rnd_target=True,
                   dmg_type='pysical', can_crit=True, true_dmg=False):

    if target_num == 'all' or target_num > len(target_party.members):
        target_num = len(target_party.members)

    members_list = target_party.members[:]
    dmg_received = 0

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

        # generate dmg
        is_crit = False
        if dmg_type == 'magic':
            dmg = attacker.int
        else:  # if dmg_type == 'physical':
            dmg = random.randint(attacker.att_dmg_min, attacker.att_dmg_max)
        if can_crit:
            if random.randrange(100) < attacker.crit_chance:
                is_crit = True
                dmg = (dmg * attacker.crit_muliplier) // 100
                print(attacker, 'hits a crit!')


        #modify dmg by attack
        dmg_dealt = dmg * dmg_mod // 100

        # target take dmg
        if dmg_type == 'true':
            dmg_multi = 1
        elif dmg_type == 'magic':
            # TODO: implement magic resi
            dmg_multi = dmg_dealt / (dmg_dealt + (target.int / 4))
        else:
            dmg_multi = dmg_dealt / (dmg_dealt + target.defense)
        dmg_done = round(dmg_dealt * dmg_multi)
        target.hp -= dmg_done

        print(attacker.name, 'hits', target.name, 'for', dmg_dealt, dmg_type, 'dmg and does', dmg_received_single, 'dmg')
        dmg_received += dmg_done
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


