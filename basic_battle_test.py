from person import Person
from Hero import Hero
from party import Party
from battle import Battle
from itertools import zip_longest
from Equipable_Items import *

# party1 = Party()
# party1.add_member(Hero.generate('Norb', 'Codesmith'))
# party1.add_member(Person.generate('Fur', 'Mage'))
# party1.add_member(Person.generate())
# party1.add_member(Person.generate())
# party2 = Party()
# party2.add_member(Person.generate())
# party2.add_member(Person.generate())
# party2.add_member(Person.generate())
# party2.add_member(Person.generate())
# battle = Battle()
# party1.party_members_info()
# party2.party_members_info()
# battle.whole_party_turn_battle(party1, party2)
# battle.alternating_turn_battle(party1, party2)

p1 = Party.generate()
p1.add_member(Person.generate('Fur', 'Jr.Coder'))
p1.add_member(Person.generate_random(1))
p1.add_member(Person.generate_random(1))
p2 = Party.generate()
p2.add_member(Person.generate('Kefka', 'Drama Queen'))
p2.add_member(Person.generate_random(1))
