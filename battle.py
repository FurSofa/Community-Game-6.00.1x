import random
from itertools import zip_longest
from x_Attack_Setups import weapon_setups
from combat_funcs import *
import random


def battle_menu(attacker, enemy_party):
    possible_actions = ['Attack', 'Spell', 'Show Hero Stats', 'Skip turn']
    action = attacker.choose_battle_action(possible_actions).lower()
    if action == 'attack':
        attack_options = [{'name': item.attack_name, 'attack_setup':item.attack_setup} for item in
                          [attacker.equip_slots['Main Hand'], attacker.equip_slots['Off Hand']] if item]

        setup_key = attacker.choose_attack(attack_options)
        setup = attack_options[setup_key]['attack_setup']
        dmg_done = run_attack(attacker, enemy_party, **setup)

    elif action == 'spell':
        # TODO: check cool downs and mana when making the list
        # attack_options = [spell for spell in attacker.spell_book]
        attack_options = []
        on_cd = []
        low_mana = []
        for spell in attacker.spell_book:
            if spell['cd_timer'] > 0:
                on_cd.append(spell)
            elif spell['mana_cost'] > attacker.tracked_values['mana']:
                low_mana.append(spell)
            else:
                attack_options.append(spell)
        if len(attack_options) < 1:
            print(f'You have no spells to use this turn!')
            action = battle_menu(attacker, enemy_party)
        else:
            setup_key = attacker.choose_attack(attack_options)
            setup = attack_options[setup_key]['attack_setup']
            dmg_done = run_attack(attacker, enemy_party, **setup)
            attacker.set_mana(-attack_options[setup_key]['mana_cost'])
            attack_options[setup_key]['cd_timer'] = attack_options[setup_key]['cool_down']

    elif action == 'show hero stats':
        attacker.party.display_single_member_item_card(attacker)
        action = battle_menu(attacker, enemy_party)

    elif action == 'heal':
        # TODO: make heal a spell, fix this!
        attacker.set_hp(attacker.stats['int'] + random.randint(-2, 3))
    elif action == 'skip turn':
        pass
    return action


def check_dodge(target, can_dodge):
    return (random.randrange(100) < target.stats['dodge']) if can_dodge else False


def check_crit(attacker, can_crit):
    return (random.randrange(100) < attacker.stats['crit_chance']) if can_crit else False


def generate_dmg(attacker, target, dmg_base='str_based', is_crit=False,
                 wpn_dmg_perc=100, c_hp_perc_dmg=0, max_hp_perc_dmg=0):

    c_hp_dmg = target.tracked_values['hp'] / 100 * c_hp_perc_dmg
    max_hp_dmg = target.stats['max_hp'] / 100 * max_hp_perc_dmg

    dmg_key = dmg_base[:3]

    with open('char_creation_setup.json') as f:
        conversion_ratios = json.load(f)['conversion_ratios']
    dmg_calc = conversion_ratios[dmg_key+'_to_dmg']

    dmg_wo_wpn = (attacker.stats[dmg_key] * dmg_calc['dmg_per_'+dmg_key]) + (attacker.level * dmg_calc['dmg_per_level'])
    wpn_dmg = round((dmg_wo_wpn / 100) * conversion_ratios['b_dmg_wpn_dmg_factor'] * attacker.stats['wpn_dmg']) + attacker.stats['wpn_dmg'] + dmg_calc['start']

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
    # if defense > dmg:
    #     dmg_done = 0
    # else:
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
               wpn_dmg_perc=100, c_hp_perc_dmg=0, max_hp_perc_dmg=0, can_dodge=True):
    """

    :param can_dodge:  bool:
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
            dmg_received = defense_calc(dmg_dealt, target, elemental,)
            target.set_hp(-dmg_received)

            if not vamp == 0:
                run_attack(attacker, attacker.party, 1, forced_primary_target=attacker,
                           primary_percent=vamp, dmg_base=dmg_base, elemental='heal',
                           can_dodge=False)

            dmg_combined += dmg_received

            verb = 'healed' if dmg_received < 0 else 'hit'
            crit_str = ' with a crit!' if is_crit else '.'
            print(f'{attacker.name} {verb} {target.name} for {abs(dmg_dealt)} pts{crit_str} {dmg_received} stuck.')
        members_list.remove(target)
        target_num -= 1
    return dmg_combined


def print_combat_status(party_1, party_2):
    def member_stat_list_generator(member):
        if member:
            stat_list = []
            stat_list.append(member.name)
            stat_list.append(member.profession)
            stat_list.append(member.tracked_values['hp'])
            stat_list.append(member.stats['max_hp'])
            # stat_list.append(member.att_dmg_min)
            # stat_list.append(member.att_dmg_max)
        else:
            return None
        return stat_list

    def member_stat_list_printer(h, e):

        if h:
            hero_name = f'{h[0]}, the {h[1]}'
            hero_hp = f'Hp: {h[2]:>2}/{h[3]:<2}'
            hero_dmg = f'Dmg: {h[4]:>2}/{h[5]:<2}'
            print(f'+ {hero_name:^23} '
                  f'{hero_hp:<8} '
                  f'{hero_dmg:<13} ', end='\t')
        else:
            print(f"{' ':<50}", end="   ")
        if e:
            enemy_name = f'{e[0]}, the {e[1]}'
            enemy_hp = f'Hp: {e[2]:>2}/{e[3]:<2}'
            enemy_dmg = f'Dmg: {e[4]:>2}/{e[5]:<2}'
            print(f'- {enemy_name:^23} '
                  f'{enemy_hp:<8} '
                  f'{enemy_dmg:<13} ', end='    \n')
        else:
            print()

    print('=' * 17, end=' ')
    print('Hero Party', end=' ')
    print('=' * 18, end='| |')
    print('=' * 18, end=' ')
    print('Enemy Party', end=' ')
    print('=' * 19, end='')
    print('')
    print('=' * 100)
    for hero, enemy in zip_longest(party_1.members, party_2.members):
        member_stat_list_printer(member_stat_list_generator(hero), member_stat_list_generator(enemy))


def single_unit_turn(unit, enemy_party):
    action = battle_menu(unit, enemy_party)
    enemy_party.remove_dead()
    return action


# TODO figure out how to justify each party output


def alternating_turn_battle(party_1, party_2):
    rounds = 0
    print('A Battle has started!')
    while party_1.has_units_left and party_2.has_units_left:
        rounds += 1
        print('\nRound:', rounds)
        print_combat_status(party_1, party_2)
        for i in range(max(len(party_1.members), len(party_2.members))):
            if i < len(party_1.members):
                action_taken = single_unit_turn(party_1.members[i], party_2)
                if not party_2.has_units_left:
                    break
            if i < len(party_2.members):
                action_taken = single_unit_turn(party_2.members[i], party_1)
                if not party_1.has_units_left:
                    break
    if party_1.has_units_left:
        party_1.party_members_info()
        print('Party 1 has won the battle!')
        input('Congrats! Press Enter!')
        for member in party_1.members:
            member.add_xp(party_2.party_worth_xp())
        party_2.__del__()

        input('Press Enter!')

    else:
        party_2.party_members_info()
        print('Party 2 has won the battle!')
    return party_1.has_units_left


def whole_party_turn_battle(party_1, party_2):
    rounds = 0
    print('A Battle has started!')
    while party_1.has_units_left and party_2.has_units_left:
        rounds += 1
        print('')
        print('Round:', rounds)
        print('Party 1:', party_1.members_names)
        print('Party 2:', party_2.members_names)
        if party_1.has_units_left:
            for member in party_1.members:
                no_enemies_left = single_unit_turn(member, party_2)
                if no_enemies_left:
                    break
                input('just press enter')
        if party_2.has_units_left:
            for member in party_2.members:
                no_enemies_left = single_unit_turn(member, party_1)
                if no_enemies_left:
                    break
                input('just press enter')
    if party_1.has_units_left:
        print('Party 1 has won the battle!')
    else:
        print('Party 2 has won the battle!')
    return party_1.has_units_left


def clock_tick(party_1, party_2):
    all_members = party_1.members + party_2.members
    for member in all_members:
        member.tracked_values['c'] += member.stats['speed']
    all_members = sorted(all_members, key=lambda m: m.tracked_values['c'], reverse=True)

    # [print(f'c: {member.tracked_values["c"]} - name: {member.name}') for member in all_members]
    return all_members


def tick_cool_downs(unit):
    for spell in unit.spell_book:
        if spell['cd_timer'] > 0:
            spell['cd_timer'] -= 1


def clock_tick_battle(party_1, party_2):
    parties = [party_1, party_2]
    print('A Battle has started!')
    c_ticks = 0
    for member in party_1.members + party_2.members:
        member.tracked_values['ct'] = 1000
        member.tracked_values['c'] = 0

    while party_1.has_units_left and party_2.has_units_left:
        all_members = clock_tick(party_1, party_2)
        c_ticks += 1
        # print(f'ticks: {c_ticks}')
        for member in all_members:
            if member.tracked_values['c'] > member.tracked_values['ct']:
                print(f'its {member.name}\'s turn!')
                both_parties = parties.copy()
                both_parties.remove(member.party)
                enemy_party = both_parties[0]
                action_taken = single_unit_turn(member, enemy_party)
                if action_taken == 'attack':
                    member.tracked_values['c'] = 0
                    member.tracked_values['ct'] = 1000
                elif action_taken == 'spell':
                    member.tracked_values['c'] = 0
                    member.tracked_values['ct'] = 1000
                elif action_taken == 'skip turn':
                    pass
                if not enemy_party.has_units_left:
                    break
                tick_cool_downs(member)

    if party_1.has_units_left:
        print('Party 1 has won the battle!')
    else:
        print('Party 2 has won the battle!')
    return party_1.has_units_left


def initiative_battle(party_1, party_2):
    parties = [party_1, party_2]
    print('A Battle has started!')
    round = 0
    while party_1.has_units_left and party_2.has_units_left:
        print(f'Round: {round}')
        all_members = party_1.members + party_2.members
        c_round_members = sorted(all_members.copy(), key=lambda m: m.speed, reverse=True)
        while c_round_members:
            active_unit = c_round_members[0]
            both_parties = parties.copy()
            both_parties.remove(active_unit.party)
            enemy_party = both_parties[0]
            action_taken = single_unit_turn(active_unit, enemy_party)
            c_round_members.remove(active_unit)
            if not enemy_party.has_units_left:
                break
        round += 1
    if party_1.has_units_left:
        print('Party 1 has won the battle!')
    else:
        print('Party 2 has won the battle!')
    return party_1.has_units_left
