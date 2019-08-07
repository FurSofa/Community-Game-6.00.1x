from person import Person
from Hero import Hero
from party import Party
from battle import Battle
from Equipable_Items import *

party1 = Party()
party2 = Party()
battle = Battle()

hero = Hero.generate('norbnorb', 'Warrior')
hero.profession_stat_augment()

enemy = Person.generate()

party1.add_member(hero)
party2.add_member(enemy)

item = create_random_equipable_item(1, 1)


# party2.add_member(fighter5)
# party2.add_member(fighter6)

if __name__ == '__main__':
    party1.pickup_gear(item)

    print('---------------------------------')
    print()
    #     # battle.whole_party_turn_battle(party1, party2)
    battle.alternating_turn_battle(party1, party2)
