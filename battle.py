# Contains battle logic
# TODO: Decide if class or function
from random import *
from itertools import zip_longest


class Battle:
    def __init__(self):
        pass

    def print_combat_status(self, party_1, party_2):
        def member_stat_list_generator(member):
            if member:
                stat_list = []
                stat_list.append(member.name)
                stat_list.append(member.profession)
                stat_list.append(member.hp)
                stat_list.append(member.max_hp)
                stat_list.append(member.dam_min)
                stat_list.append(member.dam_max)
            else:
                return None
            return stat_list

        def member_stat_list_printer(h, e):

            if h:
                hero_name = f'{h[0]}, the {h[1]}'
                hero_hp = f'Hp: {h[2]:>2}/{h[3]:<2}'
                hero_dmg = f'Dmg: {h[4]:>2}/{h[5]:<2}'
                print(f'- {hero_name:^23} '
                      f'{hero_hp:<8} '
                      f'{hero_dmg:<13} ', end='\t')
            else:
                print(f"{' ':<29}", end=" | ")
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

    def single_unit_turn(self, unit, enemy_party):
        print(unit, 'has to choose an action.')
        unit.battle_turn(enemy_party)
        enemy_party.remove_dead()
        return not enemy_party.has_units_left

    def whole_party_turn_battle(self, party_1, party_2):
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
                    no_enemies_left = self.single_unit_turn(member, party_2)
                    if no_enemies_left:
                        break
                    input('just press enter')
            if party_2.has_units_left:
                for member in party_2.members:
                    no_enemies_left = self.single_unit_turn(member, party_1)
                    if no_enemies_left:
                        break
                    input('just press enter')
        if party_1.has_units_left:
            print('Party 1 has won the battle!')
        else:
            print('Party 2 has won the battle!')
        return party_1.has_units_left

        # TODO figure out how to justify each party output

    def alternating_turn_battle(self, party_1, party_2):
        rounds = 0
        print('A Battle has started!')
        while party_1.has_units_left and party_2.has_units_left:
            rounds += 1
            print('Round:', rounds)
            print('Party 1:')
            party_1.party_members_info()
            print('Party 2:')
            party_2.party_members_info()
            for i in range(max(len(party_1.members), len(party_2.members))):
                if i < len(party_1.members):
                    no_enemies_left = self.single_unit_turn(party_1.members[i], party_2)
                    if no_enemies_left:
                        break
                    input('just press enter')
                if i < len(party_2.members):
                    no_enemies_left = self.single_unit_turn(party_2.members[i], party_1)
                    if no_enemies_left:
                        break
                    input('just press enter')
        if party_1.has_units_left:
            party_1.party_members_info()
            print('Party 1 has won the battle!')
        else:
            party_2.party_members_info()
            print('Party 2 has won the battle!')
        return party_1.has_units_left


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
            print(f"{' ':<48}", end=" | ")
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
    print('\n', unit.show_combat_stats(), 'has to choose an action.')
    unit.battle_turn(enemy_party)
    enemy_party.remove_dead()
    return not enemy_party.has_units_left


def whole_party_turn_battle(party_1, party_2):
    rounds = 0
    print('A Battle has started!')
    while party_1.has_units_left and party_2.has_units_left:
        rounds += 1
        print('')
        print('Round:', rounds)

        if party_1.has_units_left:
            for member in party_1.members:
                no_enemies_left = single_unit_turn(member, party_2)
                if no_enemies_left:
                    break
        if party_2.has_units_left:
            for member in party_2.members:
                no_enemies_left = single_unit_turn(member, party_1)
                if no_enemies_left:
                    break
    if party_1.has_units_left:
        print('Your party has won the battle!')
    else:
        print('Enemy party has won the battle!')
    return party_1.has_units_left

    # TODO figure out how to justify each party output


def alternating_turn_battle(party_1, party_2):
    rounds = 0
    print('A Battle has started!')
    while party_1.has_units_left and party_2.has_units_left:
        rounds += 1
        print('Round:', rounds)
        print_combat_status(party_1, party_2)
        for i in range(max(len(party_1.members), len(party_2.members))):
            if i < len(party_1.members):
                no_enemies_left = single_unit_turn(party_1.members[i], party_2)
                if no_enemies_left:
                    break
            if i < len(party_2.members):
                no_enemies_left = single_unit_turn(party_2.members[i], party_1)
                if no_enemies_left:
                    break
    if party_1.has_units_left:
        party_1.party_members_info()
        print('Party 1 has won the battle!')
        for member in party_1.members:
            member.add_xp(party_2.party_worth_xp())
        party_2.__del__()
        input('Congrats! Press Enter!')
    else:
        party_2.party_members_info()
        print('Party 2 has won the battle!')
    return party_1.has_units_left


def battle(party_1, party_2):
    pass
