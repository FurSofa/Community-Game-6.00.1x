# Testing Grounds!
"""
Use this space to test out features!
"""
from person import Person
from Hero import Hero
from party import Party
from battle import *
from Equipable_Items import *

['Great', 'Weapon' 'Main Hand' '10/' '10' '2-' '3']
['Legendary', 'Weapon' 'Off Hand' '10/' '10' '2-' '3']
['Magical', 'Armor' 'Head' '5']

def print_combat_status(party_1, party_2):
    def item_stat_list_generator(i):
        if i:
            stat_list = []
            stat_list.append(i.quality.title())
            stat_list.append(i.etype.title())
            stat_list.append(i.equipable_slot.title())
            stat_list.append(i.)
            stat_list.append(i.)
            stat_list.append(i.)
        else:
            return None
        return stat_list
    def member_stat_list_printer(x, y, z):

        if x:
            x_name = f'{x[0]} {x[1]}'

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
        print(f'{item_1_name}{}{}')

    print('=' * 17, end=' ')
    print('Hero Party', end=' ')
    print('=' * 18, end='| |')
    print('=' * 18, end=' ')
    print('Enemy Party', end=' ')
    print('=' * 19, end='')
    print('')
    print('=' * 100)
    for hero, enemy in zip_longest(party_1.members, party_2.members):
        member_stat_list_printer(item_stat_list_generator(list_1), item_stat_list_generator(list_2))

print('===  From Test File  ===')
h = Party()
h.add_item(Weapon.generate_random())
h.add_item(Armor.generate_random())
h.add_item(Armor.generate_random())
h.show_gear(h.inventory)
