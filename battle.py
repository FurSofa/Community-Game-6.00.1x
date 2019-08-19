import random
from itertools import zip_longest
from attack_setups import weapon_setups
from combat_funcs import *
import random


def battle_menu(attacker, enemy_party):
    possible_actions = ['Attack', 'Heal', 'Show Hero Stats', 'Skip turn']
    action = attacker.choose_battle_action(possible_actions).lower()
    if action == 'attack':
        # TODO: make this independent of setup file! (get the setup from the weapon)
        attack_options = [item.attack_name for item in
                          [attacker.equip_slots['Main Hand'], attacker.equip_slots['Off Hand']] if item]

        setup_key = attacker.choose_attack(attack_options)
        setup = weapon_setups[setup_key]
        dmg_done = run_attack(attacker, enemy_party, **setup)

    elif action == 'show hero stats':
        attacker.party.display_single_member_item_card(attacker)
        battle_menu(attacker, enemy_party)
    elif action == 'heal':
        # TODO: make heal a spell, fix this!
        attacker.set_hp(attacker.int + random.randint(-2, 3))

    elif action == 'skip turn':
        pass
    return action


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
        else:  # if dmg_base == 'physical':
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

        print(attacker.name, 'hits', target.name, 'for', dmg_dealt, dmg_type, 'dmg and does', dmg_done, 'dmg')
        dmg_received += dmg_done
        members_list.remove(target)
        target_num -= 1
    return dmg_received


def print_combat_status(party_1, party_2):
    def member_stat_list_generator(member):
        if member:
            stat_list = []
            stat_list.append(member.name)
            stat_list.append(member.profession)
            stat_list.append(member.hp)
            stat_list.append(member.max_hp)
            stat_list.append(member.att_dmg_min)
            stat_list.append(member.att_dmg_max)
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


def battle(party_1, party_2):
    pass


empty = 'Empty'
print(f'{empty:^30}')
