# Contains battle logic
# TODO: should this be a function call or a class?
from itertools import zip_longest


class Battle:
    def __init__(self):
        pass

    def single_unit_turn(self, unit, enemy_party):
        print(unit, 'has to choose an action.')
        unit.choose_battle_action(enemy_party)
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

    def part_1(selfs, party_1):
        print_list_1 = []
        for member in party_1:
            member_stats = []
            member_stats.append(member.name)
            member_stats.append(member.profession)
            member_stats.append(member.level)
            member_stats.append(member.hp)
            member_stats.append(member.max_hp)
            print_list_1.append(member_stats)
        return print_list_1

    def part_2(selfs, party_2):
        print_list_2 = []
        for member in party_2:
            member_stats = []
            member_stats.append(member.name)
            member_stats.append(member.profession)
            member_stats.append(member.level)
            member_stats.append(member.hp)
            member_stats.append(member.max_hp)
            print_list_2.append(member_stats)
        return print_list_2

    def print_party_lists(self, list_1, list_2):

        for i, j in zip_longest(list_1, list_2, fillvalue=''):
            for x, y in zip_longest(i, j,fillvalue=''):
                print(f'- {x[0]}, {x[1]} Lv: {x[2]} {x[3]}/{x[4]}',
                      f'- {y[0]}, {y[1]} Lv: {y[2]} {y[3]}/{y[4]}')

    def party_vs_party(self, party_1, party_2):

        print('=' * 9, 'Hero Party', '=' * 9, end=" ")
        print('=' * 9, 'Enemy Party', '=' * 9, end='\n')
        self.print_party_lists(self.part_2(party_1), self.part_2(party_2))

        # for i, j in zip_longest(print_list_1, print_list_2, fillvalue=''):
        #     print(f'- {heroes.name}, {heroes.profession} Lv: {heroes.level} {heroes.hp}/{heroes.max_hp}',
        #           f'- {enemies.name}, {enemies.profession} Lv: {enemies.level} {enemies.hp}/{enemies.max_hp}')
        # TODO figure out how to justify each party output

    def alternating_turn_battle(self, party_1, party_2):
        rounds = 0
        print('A Battle has started!')
        while party_1.has_units_left and party_2.has_units_left:
            rounds += 1
            print('Round:', rounds)
            self.party_vs_party(party_1.members, party_2.members)
            # print('Party 1:', party_1.members_names)
            # print('Party 2:', party_2.members_names)
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
            print('Party 1 has won the battle!')
        else:
            print('Party 2 has won the battle!')
        return party_1.has_units_left
