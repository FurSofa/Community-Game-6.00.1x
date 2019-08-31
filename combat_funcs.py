import random
import json

from x_Attack_Setups import *  # TODO: move to json?


def battle_menu(attacker, enemy_party):
    action = attacker.choose_battle_action(enemy_party).lower()

    if action == 'attack':
        # TODO: make this independent of setup file! (get the setup from the weapon)
        attack_options = [item['attack_name'] for item in
                          [attacker.equip_slots['Main Hand'], attacker.equip_slots['Off Hand']] if item]

        setup_key = attacker.choose_attack(attack_options)
        setup = weapon_setups[setup_key]
        dmg_done = run_attack(attacker, enemy_party, **setup)

    elif action == 'show hero stats':
        attacker.party.display_single_member_item_card(attacker)
        battle_menu(attacker, enemy_party)

    elif action == 'heal':
        attacker.heal(attacker.calculate_dmg())


def check_dodge(target, can_dodge):
    return (random.randrange(100) < target.dodge) if can_dodge else False


def check_crit(attacker, can_crit):
    return (random.randrange(100) < attacker.crit_chance) if can_crit else False


def generate_dmg(attacker, target, dmg_base='str_based', is_crit=False,
                 wpn_dmg_perc=100, c_hp_perc_dmg=0, max_hp_perc_dmg=0):

    c_hp_dmg = target.tracketd_values['hp'] / 100 * c_hp_perc_dmg
    max_hp_dmg = target.stats['max_hp'] / 100 * max_hp_perc_dmg

    dmg_key = dmg_base[:3]

    with open('char_creation_setup.json') as f:
        growths_ratios = json.load(f)['growth_ratios']
    dmg_calc = growths_ratios[dmg_key+'_to_dmg']

    dmg_wo_wpn = (attacker.stats[dmg_key] * dmg_calc['dmg_per_'+dmg_key]) + (attacker.level * dmg_calc['dmg_per_level'])
    wpn_dmg = round((dmg_wo_wpn / 100) * growths_ratios['b_dmg_wpn_dmg_factor'] * attacker.stats['wpn_dmg']) + attacker.stats['wpn_dmg'] + dmg_calc['start']

    wpn_dmg = wpn_dmg / 100 * wpn_dmg_perc

    dmg = sum([c_hp_dmg, max_hp_dmg, wpn_dmg])
    if is_crit:
        dmg = (dmg * attacker.stats["crit_dmg"]) // 100
    return round(dmg)


def defense_calc(dmg, target, elemental):
    # TODO: generalise resistances
    # if not elemental == 'physical':
    #     dmg_multi = dmg / (dmg + target.__dict__[elemental + '_res'])
    # else:
    #     dmg_multi = dmg / (dmg + target.defense)
    # dmg_done = round(dmg * dmg_multi)
    if elemental == 'physical':  # untill we have the new npc
        defense = target.stats['armor']
    elif elemental == 'magic':
        defense = target.stats['magic_resistance']
    elif elemental == 'elemental':
        defense = target.stats['elemental_resistance']
    else:
        defense = 0  # TODO: heal reduction/multi?
    # TODO: armor piercing calc here
    if defense > dmg:
        dmg_done = 0
    else:
        if defense < 0:
            lol_dmg_multi = 2 - (100 / (100 - defense))
        else:
            lol_dmg_multi = 100 / (100 + defense)

        dmg_done = lol_dmg_multi * dmg

    # else:
    #     dmg_done = dmg - defense
    if elemental == 'true':
        dmg_done = dmg
    if elemental == 'heal':   # * -1 if heal
        dmg_done = -dmg_done
    return round(dmg_done)


def get_target(attacker, primary, forced_primary_target,
               target_num, members_list, rnd_target):
    if primary:
        if forced_primary_target:
            target = forced_primary_target
        else:
            target = attacker.choose_target(members_list)
    else:
        if rnd_target:
            target = random.choice(members_list)
        elif target_num < len(members_list):
            target = attacker.choose_target(members_list)
        else:
            target = members_list[0]
    return target


# TODO: add a function to modify setup based on player stats and percs once we have that before running attack?
def run_attack(attacker, target_party, target_num=1, primary=True, primary_percent=100,
               rnd_target=True, forced_primary_target=None, splash_dmg=0,
               elemental='physical', vamp=0, can_crit=True, dmg_base='str_based',
               wpn_dmg_perc=100, c_hp_perc_dmg=0, max_hp_perc_dmg=0, can_dodge=True, reduction_calc='d3'):
    """

    :param attacker: npc or subclass
    :param target_party: party
    :param target_num: int: number of targets including primary / 'all' for full target party
    :param primary: bool: is there a primary target hit for primary percent
    :param primary_percent: percent of full dmg the primary target is hit for
    :param rnd_target: bool: chooses non primary targets randomly
    :param forced_primary_target: npc or subclass: used as primary target
    :param splash_dmg: dmg to non primary targets
    :param elemental: dmg type used to calculate and apply dmg / special for 'heal'(inverts dmg) and 'true'(ignores defense)
    :param vamp: int: percentage of dmg dealt affecting attacker hp. can be negative
    :param can_crit: bool:
    :param dmg_base: 'str_based' or 'int_based'. for dmg generation
    :param max_hp_perc_dmg: int: percent of target max hp as dmg
    :param c_hp_perc_dmg: int: percent of target current hp as dmg
    :param wpn_dmg_perc: int: percentage modifier for weapon dmg / set to 0 if you want only target hp pool based dmg
    :return: int: overall dmg done
    """
    members_list = attacker.party.members[:] if elemental == 'heal' else target_party.members[:]

    if target_num == 'all' or target_num > len(members_list):
        target_num = len(members_list)

    dmg_combined = 0
    while target_num > 0:
        dmg_mod = primary_percent if primary else splash_dmg
        target = get_target(attacker, primary, forced_primary_target, target_num,
                            members_list, rnd_target)
        primary = False
        is_crit = check_crit(attacker, can_crit)
        raw_dmg = generate_dmg(attacker, target, dmg_base, is_crit, wpn_dmg_perc,
                               c_hp_perc_dmg, max_hp_perc_dmg, )  # value for full dmg before and mod or reduction

        #  other modification, not really generation, not really defense reduction
        dmg_dealt = raw_dmg * dmg_mod // 100  # modify for splash or primary dmg factor
        is_dodge = check_dodge(target, can_dodge)
        if is_dodge:
            pass
            print(f'{target.name} dodged!')
        else:
            dmg_received = defense_calc(attacker, dmg_dealt, target, elemental, reduction_calc)
            target.set_hp(-dmg_received)

            if not vamp == 0:
                run_attack(attacker, attacker.party, 1, forced_primary_target=attacker,
                           primary_percent=vamp, dmg_base=dmg_base, elemental='heal',
                           reduction_calc=reduction_calc, can_dodge=False)

            dmg_combined += dmg_received

            verb = 'healed' if dmg_received < 0 else 'hit'
            crit_str = ' with a crit!' if is_crit else '.'
            print(f'{attacker.name} {verb} {target.name} for {abs(dmg_dealt)} pts{crit_str} {dmg_received} stuck.')
        members_list.remove(target)
        target_num -= 1
    return dmg_combined
