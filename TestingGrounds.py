# Testing Grounds!
"""
Use this space to test out features!
"""
from person import Person
from Hero import Hero
from party import Party
from battle import Battle
from Equipable_Items import *

if __name__ == "__main__":
# Testing code!
    print('     Creating Hero party!')

    hero_party = Party()
    h1 = Hero.generate_random()
    p1 = Person.generate_random()
    hero_party.add_member(h1)
    hero_party.add_member(p1)
    hero_party.party_members_info()
    print('\n')
    print('     Creating Enemy party!')
    enemy_party = Party()
    e1 = Person.generate_random()
    e2 = Person.generate_random()
    enemy_party.add_member(e1)
    enemy_party.add_member(e2)
    enemy_party.party_members_info()
    print('Done! You now have two parties')


    def Fur_tests(n=10):
        pass


    Fur_tests()
