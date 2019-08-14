# Testing Grounds!
"""
Use this space to test out features!
"""
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


def print_inventory1(card_list):
    # Print Top
    print("┌" + "─" * 32 + "┬" + "─" * 32 + "┬" + "─" * 32 + "┐")
    # Print inventory
    i = 0
    j, k, l = 0, 1, 2
    while i < 3:
        print("\n".join(f'│ {x} │ {y} │ {z} │' for x, y, z in
                        zip(card_list[j].splitlines(), card_list[k].splitlines(), card_list[l].splitlines())))
    j += 3
    k += 3
    l += 3
    i += 1

    # Print Bottom
    print("└" + "─" * 32 + "┴" + "─" * 32 + "┴" + "─" * 32 + "┘")

def print_inventory(inventory):
    empty_card = [" " * 30] * 3
    cards = [item.item_card() if item else empty_card for item in inventory + (9 - len(inventory)) * [None]]
    inv = ' Party Inventory '
    print(f'{inv:^100}')
    print(" ┌" + "─" * 32 + "┬" + "─" * 32 + "┬" + "─" * 32 + "┐ ")
    print("\n".join(f' │ {x} │ {y} │ {z} │ ' for x,y,z in zip(*cards[:3])))
    print(" ├" + "─" * 32 + "┼" + "─" * 32 + "┼" + "─" * 32 + "┤ ")
    print("\n".join(f' │ {x} │ {y} │ {z} │ ' for x,y,z in zip(*cards[3:6])))
    print(" ├" + "─" * 32 + "┼" + "─" * 32 + "┼" + "─" * 32 + "┤ ")
    print("\n".join(f' │ {x} │ {y} │ {z} │ ' for x,y,z in zip(*cards[6:])))
    print(" └" + "─" * 32 + "┴" + "─" * 32 + "┴" + "─" * 32 + "┘ ")

if __name__ == '__main__':
    print('===  From Test File  ===')
    h = Party()
    h.add_item(Weapon.generate_random())
    h.add_item(Weapon.generate_random())
    h.add_item(Weapon.generate_random())
    h.add_item(Armor.generate_random())
    h.add_item(Armor.generate_random())
    h.add_item(Armor.generate_random())
    h.add_item(Armor.generate_random())
    h.add_item(Armor.generate_random())
    h.add_item(Armor.generate_random())
    h.print_inventory()
    print_inventory(h.inventory)
    print(len('                                         '))
    print(len('                                          '))
