from person import Person
from Hero import Hero
from party import Party
from battle import Battle
from Equipable_Items import *

party1 = Party()
party2 = Party()
battle = Battle()


party1.add_member(Hero.generate('Norb', 'Codesmith'))
party1.add_member(Person.generate('Fur', 'Mage'))
# party1.add_member(Person.generate())
# party1.add_member(Person.generate())

party2.add_member(Person.generate())
party2.add_member(Person.generate())
# party2.add_member(Person.generate())
# party2.add_member(Person.generate())


# party1.party_members_info()
# party2.party_members_info()


# if __name__ == "__main__":
#     print('---------------------------------')
#     print()
#     #     # battle.whole_party_turn_battle(party1, party2)
battle.alternating_turn_battle(party1, party2)


"""
===== Hero Party Members ===== ===== Enemy Party Members =====
  Members:                          Members:
- Hero, Warrior Lv: 1 60/60       - Jeb, Warrior Lv: 1 70/70
- Jeb, Warrior Lv: 1 70/70        - Jeb, Warrior Lv: 1 65/65


"""