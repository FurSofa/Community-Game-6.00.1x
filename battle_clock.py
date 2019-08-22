from person import NPC
from Hero import Hero
from party import Party
from Item_Bases import *
import random
from combat_funcs import *
from attack_setups import *
from battle import *


class DGame:
    def __init__(self, difficulty):
        self.difficulty = difficulty

dummy_game = DGame('Easy')


p1 = Party.generate(dummy_game)
p1.add_member(Hero.generate('Fur', 'Jr.Coder'))
p1.add_member(NPC.generate_random())

p2 = Party.generate(dummy_game)
p2.add_member(NPC.generate('Kefka', 'Drama Queen'))
p2.add_member(NPC.generate_random())
p2.add_member(NPC.generate_random())

p1.add_item(create_random_equipable_item(5, etype=1))
p2.add_item(create_random_equipable_item(5, etype=1))


per1 = p1.members[0]
pers2 = p2.members[0]

per1.hp -= 20


parties = [p1, p2]

elemental_list = ['fire', 'ice', 'holy', 'water']
for party in parties:
    for member in party.members:
        member.__dict__['ct'] = 100
        member.__dict__['speed'] = member.dex + random.randint(1, 7)
        member.__dict__['c'] = 0
        for e in elemental_list:
            member.__dict__[e + '_res'] = random.randint(-10, 20)

#
# def clock_tick(party_1, party_2):
#     all_members = party_1.members + party_2.members
#     for member in all_members:
#         member.c += member.speed
#     all_members = sorted(all_members, key=lambda m: m.c, reverse=True)
#
#     [print(f'c: {member.c} - name: {member.name}') for member in all_members]
#     return all_members
#
#
# def clock_tick_battle(party_1, party_2):
#     parties = [party_1, party_2]
#     print('A Battle has started!')
#     c_ticks = 0
#     for member in party_1.members + party_2.members:
#         member.ct = 100
#         member.c = 0
#
#     while party_1.has_units_left and party_2.has_units_left:
#         all_members = clock_tick(party_1, party_2)
#         c_ticks += 1
#         print(f'ticks: {c_ticks}')
#         for member in all_members:
#             if member.c > member.ct:
#                 print(f'its {member.name}\'s turn!')
#                 both_parties = parties.copy()
#                 both_parties.remove(member.party)
#                 enemy_party = both_parties[0]
#                 action_taken = single_unit_turn(member, enemy_party)
#                 if action_taken == 'attack':
#                     member.c = 0
#                     member.ct = 100
#                 elif action_taken == 'heal':
#                     member.c = 0
#                     member.ct = 80
#                 elif action_taken == 'skip turn':
#                     pass
#                 if not enemy_party.has_units_left:
#                     break
#     if party_1.has_units_left:
#         print('Party 1 has won the battle!')
#     else:
#         print('Party 2 has won the battle!')
#     return party_1.has_units_left
#
#
# def initiative_battle(party_1, party_2):
#     parties = [party_1, party_2]
#     print('A Battle has started!')
#     round = 0
#     while party_1.has_units_left and party_2.has_units_left:
#         print(f'Round: {round}')
#         all_members = party_1.members + party_2.members
#         c_round_members = sorted(all_members.copy(), key=lambda m: m.speed, reverse=True)
#         while c_round_members:
#             active_unit = c_round_members[0]
#             both_parties = parties.copy()
#             both_parties.remove(active_unit.party)
#             enemy_party = both_parties[0]
#             action_taken = single_unit_turn(active_unit, enemy_party)
#             c_round_members.remove(active_unit)
#             if not enemy_party.has_units_left:
#                 break
#         round += 1
#     if party_1.has_units_left:
#         print('Party 1 has won the battle!')
#     else:
#         print('Party 2 has won the battle!')
#     return party_1.has_units_left
