# Testing Grounds!
"""
Use this space to test out features!
"""
import Game
from person import Person
from Hero import Hero
from party import Party
from battle import *
from Item_Bases import *


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
    print("└" + "─" * 23 + "┴" + "─" * 23 + "┴" + "─" * 23 + "┴" + "─" * 23 + "┘")


def display_single_member_item_card(member):
    info_card = member.info_card()
    print('-' * 8, 'Person', '-' * 9)
    print("┌" + "─" * 23 + "┐")
    print("\n".join(f'│ {x} │' for x in info_card))
    print("└" + "─" * 23 + "┘")


if __name__ == '__main__':
    print('===  From Test File  ===')
    dummy_game = {'difficulty': 'Hard'}
    h = Party(dummy_game)
    h.add_member(Person.generate_random())
    h.add_member(Person.generate_random())
    h.print_members_info_cards()
    h.display_single_member_item_card(h.member(0))

    # h.add_item(Weapon.generate(quality='Legendary', equipable_slot='Main Hand', att_dmg_max=20))
    h.add_item(create_random_equipable_item())
    h.add_item(create_random_equipable_item())
    h.add_item(create_random_equipable_item())
    h.add_item(create_random_item(2))
    h.add_item(create_random_item(2))
    h.add_item(create_random_item(2))
    h.add_item(create_random_item(1))
    h.add_item(create_random_item(1))
    h.add_item(create_random_item(1))
    h.add_item(create_random_item(1))
    h.add_item(create_random_item(1))
    h.add_item(create_random_item(1))
    h.display_inventory()

    h2 = Party(dummy_game)
    h2.add_member(Person.generate_random())
    h2.add_member(Person.generate_random())
    h2.add_item(create_random_item(2))
    h2.add_item(create_random_item(1))
