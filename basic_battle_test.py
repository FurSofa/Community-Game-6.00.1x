from person import NPC
from Hero import Hero
from party import Party
from battle import *
from battle import Battle
from itertools import zip_longest
from Item_Bases import *
from combat_funcs import *

# party1 = Party()
# party1.add_member(Hero.generate('Norb', 'Codesmith'))
# party1.add_member(NPC.generate('Fur', 'Mage'))
# party1.add_member(NPC.generate())
# party1.add_member(NPC.generate())
# party2 = Party()
# party2.add_member(NPC.generate())
# party2.add_member(NPC.generate())
# party2.add_member(NPC.generate())
# party2.add_member(NPC.generate())
# battle = Battle()
# party1.party_members_info()
# party2.party_members_info()
# battle.whole_party_turn_battle(party1, party2)
# battle.alternating_turn_battle(party1, party2)
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

# print_combat_status(p1, p2)

# while p1.has_units_left:
#
#     alternating_turn_battle(p1, p2)
#     p1.heal_everyone()
#
#     p2.add_member(NPC.generate_random(1))
#     p2.add_member(NPC.generate_random(1))
