from person import NPC
from Hero import Hero
from party import Party
from Item_Bases import *
import random
from combat_funcs import *
from attack_setups import *
from battle import *


dummy_game = {'difficulty': 'Hard'}

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

def clock_tick(parties):
    # all_members = [member for member in party.members for party in parties]
    all_members = p1.members + p2.members
    for member in all_members:
        member.c += member.speed
    all_members = sorted(all_members, key=lambda m: m.c, reverse=True)

    [print(f'c: {member.c} - name: {member.name}') for member in all_members]

    for member in all_members:
        if member.c > member.ct:
            print(f'its {member.name}\'s turn!')
            member.c = 0
