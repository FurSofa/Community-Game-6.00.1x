# Testing Grounds!
"""
Use this space to test out features!
"""
import Game
from person import Person
from Hero import Hero
from party import Party
from battle import *
from Equipable_Items import *

# Original text generator
# print("┌" + "─" * 32 + "┬" + "─" * 32 + "┬" + "─" * 32 + "┐")
# print("\n".join(f'│ {x} │ {y} │ {z} │' for x, y, z in zip(card1.splitlines(), card2.splitlines(), card3.splitlines())))
# print("└" + "─" * 32 + "┴" + "─" * 32 + "┴" + "─" * 32 + "┘")

"""
┌───────────────────────────────┬────────────────────────────────┬───────────────────────────────┐ # len(98)
│Dirty Hat                 Head │ Gold Necklace             Neck │ Epic Sword           Main Hand│
│Dur: 13/100    Damage:  NA-NA  │ Dur: NA/NA     Damage:  NA-NA  │ Dur: 3000/3000 Damage: 100-100│
└───────────────────────────────┴────────────────────────────────┴───────────────────────────────┘
"""


# def generate_card_list(inventory):
#     card_list = []
#     empty_card = ['                              ',
#                   '            Empty             ',
#                   '                              ']
#     for item in inventory:
#         card_list.append(item.item_card)
#
#     for item in inventory + (9 - len(inventory)) * [None]:
#         if item:
#             card_list.append(item.item_card)
#         else:
#             card_list.append(empty_card)
#     return card_list


def print_inventory_default(inventory):
    empty_card = [" " * 30] * 3
    cards = [item.item_card() if item else empty_card for item in inventory + (9 - len(inventory)) * [None]]
    inv = ' Party Inventory '
    print('=' * 41, 'Party Inventory', '=' * 42)
    print("┌" + "─" * 32 + "┬" + "─" * 32 + "┬" + "─" * 32 + "┐")
    print("\n".join(f'│ {x} │ {y} │ {z} │ ' for x, y, z in zip(*cards[:3])))
    print("├" + "─" * 32 + "┼" + "─" * 32 + "┼" + "─" * 32 + "┤")
    print("\n".join(f'│ {x} │ {y} │ {z} │ ' for x, y, z in zip(*cards[3:6])))
    print("├" + "─" * 32 + "┼" + "─" * 32 + "┼" + "─" * 32 + "┤")
    print("\n".join(f'│ {x} │ {y} │ {z} │ ' for x, y, z in zip(*cards[6:])))
    print("└" + "─" * 32 + "┴" + "─" * 32 + "┴" + "─" * 32 + "┘")


def print_single_item_card(item):
    x = item.item_card()
    print("┌" + "─" * 30 + "┐")
    print("\n".join(f'│ {x[0]} │'))
    print("├" + "─" * 30 + "┤")
    print("\n".join(f'│ {x[1]} │'))
    print("├" + "─" * 30 + "┤")
    print("\n".join(f'│ {x[2]} │'))
    print("└" + "─" * 30 + "┘")


def print_member_info_cards(members):
    empty_card = [" " * 21] * 6
    cards = [member.info_card() if member else empty_card for member in members
             + (16 - len(members)) * [None]]

    print('=' * 41, 'Party Members', '=' * 42)
    print("┌" + "─" * 23 + "┬" + "─" * 23 + "┬" + "─" * 23 + "┬" + "─" * 23 + "┐")
    print("\n".join(f'│ {w} │ {x} │ {y} │ {z} │ ' for w, x, y, z in zip(*cards[:4])))
    if len(members) > 3:
        print("├" + "─" * 23 + "┼" + "─" * 23 + "┼" + "─" * 23 + "┼" + "─" * 23 + "┤")
        print("\n".join(f'│ {w} │ {x} │ {y} │ {z} │ ' for w, x, y, z in zip(*cards[4:8])))
    if len(members) > 6:
        print("├" + "─" * 23 + "┼" + "─" * 23 + "┼" + "─" * 23 + "┼" + "─" * 23 + "┤")
        print("\n".join(f'│ {w} │ {x} │ {y} │ {z} │ ' for w, x, y, z in zip(*cards[8:12])))
    if len(members) > 6:
        print("├" + "─" * 23 + "┼" + "─" * 23 + "┼" + "─" * 23 + "┼" + "─" * 23 + "┤")
        print("\n".join(f'│ {w} │ {x} │ {y} │ {z} │ ' for w, x, y, z in zip(*cards[12:16])))
    print("└" + "─" * 23 + "┴" + "─" * 23 + "┴" + "─" * 23+ "┴" + "─" * 23 + "┘")


if __name__ == '__main__':
    print('===  From Test File  ===')
    h = Party()
    h.add_member(Person.generate_random())
    h.add_member(Person.generate_random())
    h.add_member(Person.generate_random())
    h.add_member(Person.generate_random())
    h.add_member(Person.generate_random())

    h.add_item(Weapon.generate(quality='Legendary', equipable_slot='main hand', att_dmg_max=20))
    h.add_item(Armor.generate(equipable_slot='Chest'))

    h.display_single_member_item_card(h.member(0))


