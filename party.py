from helper_functions import *
from Hero import *
from person import *
from Equipable_Items import *


class Party:
    def __init__(self, game):
        self.hero = None
        self.members = []
        self.dead_members = []
        # inventory
        self.inventory = []
        self.equipment = []  # used for armor and weapons
        self.gold = 0

        self.game = game

    def __str__(self):
        return 'h: ' + str(self.hero()) + ' ' + str(self.members)

    @classmethod
    def generate(cls, game):
        return cls(game)

    @classmethod
    def __del__(cls):
        del cls

    def alive(self):
        """ Checks if anyone is alive
        :returns True if any party member is alive
        """
        return any([member.is_alive for member in self.members])

    def kill_everyone(self):
        delete_index = []
        for i, member in enumerate(self.members):
            delete_index.append(i)
        for i in reversed(delete_index):
            self.dead_members.append(self.members.pop(i))

    def heal_everyone(self):
        for member in self.members:
            member.heal(member.max_hp)

    def party_members_info(self):
        print('\n', '=' * 6, 'Party Members Info', '=' * 6)
        for member in self.members:
            print(f'- {member.name}, {member.profession} Lv: {member.level} {member.hp}/{member.max_hp}')

    def print_members_info_cards(self):
        empty_card = [" " * 21] * 6
        cards = [member.info_card() if member else empty_card for member in self.members
                 + (16 - len(self.members)) * [None]]

        print('=' * 41, 'Party Members', '=' * 42)
        print("┌" + "─" * 23 + "┬" + "─" * 23 + "┬" + "─" * 23 + "┬" + "─" * 23 + "┐")
        print("\n".join(f'│ {w} │ {x} │ {y} │ {z} │ ' for w, x, y, z in zip(*cards[:4])))
        if len(self.members) > 3:
            print("├" + "─" * 23 + "┼" + "─" * 23 + "┼" + "─" * 23 + "┼" + "─" * 23 + "┤")
            print("\n".join(f'│ {w} │ {x} │ {y} │ {z} │ ' for w, x, y, z in zip(*cards[4:8])))
        if len(self.members) > 6:
            print("├" + "─" * 23 + "┼" + "─" * 23 + "┼" + "─" * 23 + "┼" + "─" * 23 + "┤")
            print("\n".join(f'│ {w} │ {x} │ {y} │ {z} │ ' for w, x, y, z in zip(*cards[8:12])))
        if len(self.members) > 12:
            print("├" + "─" * 23 + "┼" + "─" * 23 + "┼" + "─" * 23 + "┼" + "─" * 23 + "┤")
            print("\n".join(f'│ {w} │ {x} │ {y} │ {z} │ ' for w, x, y, z in zip(*cards[12:16])))
        print("└" + "─" * 23 + "┴" + "─" * 23 + "┴" + "─" * 23 + "┴" + "─" * 23 + "┘")

    @staticmethod
    def display_single_member_item_card(member):
        info_card = member.info_card()
        print('-' * 8, 'Person', '-' * 9)
        print("┌" + "─" * 23 + "┐")
        print("\n".join(f'│ {x} │' for x in info_card))
        print("└" + "─" * 23 + "┘")

    @property
    def has_units_left(self) -> bool:
        """
        checks if active members are left
        :return: True if any party member is alive
        """
        return len(self.members) > 0

    @property
    def members_names(self):
        """
        :return: string of active members separated my ','
        """
        return ', '.join(member.name for member in self.members)

    def members_names_list(self):
        """
        :return: string of active members separated my ','
        """
        return [member.name for member in self.members]

    def member(self, position=0):
        """
        :return: party member class @ position
        :Use: Used to access member.Method()
        """
        return self.members[position]

    def hero(self):
        """
        :return: returns the hero or None
        """
        heroes = [member.name for member in self.members if member.is_alive and isinstance(member, Hero)]
        if heroes:
            return heroes[0]
        else:
            return None

    def has_hero(self):
        """ Checks if anyone is alive
        :returns True if any party member is a hero
        """
        return any([isinstance(member, Hero) for member in self.members])

    def remove_dead(self):
        """
        removes dead players from active members and places them in dead members
        :return: number of members found dead
        """
        delete_index = []
        for i, member in enumerate(self.members):
            if not member.is_alive:
                delete_index.append(i)
                print(member.name, 'is dead!')
        for i in reversed(delete_index):
            self.dead_members.append(self.members.pop(i))
        return len(delete_index)

    def party_worth_xp(self):
        return len(self.dead_members) * 5

    def add_member(self, member):
        """
        adds a member to the party
        :param member: Person or Hero class object
        :return:
        """
        print(f'{member.name}, the {member.profession} joins the party!')
        member.party = self
        self.members.append(member)
        if member.hero:
            self.hero = member

    #  inventory and trading

    def inventory_menu(self):
        self.display_inventory()
        x = select_from_list(['Inventory', 'Character Inventory', 'Exit'], '', True, False)
        if x == 0:
            # Inventory
            self.display_inventory()
            selection = select_from_list(['Equip', 'Repair', 'Sell', 'Exit'], '', True, True)
            if selection == 0:
                # Equip
                self.display_inventory()
                if len(self.inventory) == 0:
                    print('You have no items!')
                else:
                    item = select_from_list(self.inventory,
                                            'Which Item would you like to equip?', True, True)
                    character = select_from_list(self.members_names_list(),
                                                 'Who do you want to equip this item?', True, True)
                    self.equip_gear(self.members[character], self.inventory[item])
                self.inventory_menu()
            elif selection == 1:
                # Repair
                self.display_inventory()
                item = select_from_list(['', '', '', '', '', '', '', '', ''],
                                        'Which Item would you like to repair?', True, True)

                self.inventory[item].repair()
                self.inventory_menu()
            elif selection == 2:
                # Sell
                self.display_inventory()
                item = select_from_list(['', '', '', '', '', '', '', '', ''],
                                        'Which Item would you like to sell?', True, True)

                # self.gold += self.inventory[item].value
                self.inventory.pop(item)
                self.inventory_menu()
            elif selection == 3:
                pass

        if x == 1:
            # Char Inventory
            # TODO: Install char equipment output. "Reuse inventory output?"
            char = select_from_list(self.members_names_list(),
                                    'Who do you want to view?', True, True)
            self.members[char].show_stats()
            self.members[char].get_equipped_items()
        if x == 2:
            # Exit
            pass

    def display_inventory(self):
        empty_card = [" " * 30] * 3
        cards = [item.item_card() if item else empty_card for item in self.inventory
                 + (15 - len(self.inventory)) * [None]]
        print('\n' * 20)
        print('=' * 41, 'Party Inventory', '=' * 42)
        print("┌" + "─" * 32 + "┬" + "─" * 32 + "┬" + "─" * 32 + "┐")
        print("\n".join(f'│ {x} │ {y} │ {z} │' for x, y, z in zip(*cards[:3])))
        if len(self.inventory) > 3:
            print("├" + "─" * 32 + "┼" + "─" * 32 + "┼" + "─" * 32 + "┤")
            print("\n".join(f'│ {x} │ {y} │ {z} │ ' for x, y, z in zip(*cards[3:6])))
        if len(self.inventory) > 6:
            print("├" + "─" * 32 + "┼" + "─" * 32 + "┼" + "─" * 32 + "┤")
            print("\n".join(f'│ {x} │ {y} │ {z} │ ' for x, y, z in zip(*cards[6:9])))
        if len(self.inventory) > 9:
            print("├" + "─" * 32 + "┼" + "─" * 32 + "┼" + "─" * 32 + "┤")
            print("\n".join(f'│ {x} │ {y} │ {z} │ ' for x, y, z in zip(*cards[9:12])))
        if len(self.inventory) > 12:
            print("├" + "─" * 32 + "┼" + "─" * 32 + "┼" + "─" * 32 + "┤")
            print("\n".join(f'│ {x} │ {y} │ {z} │ ' for x, y, z in zip(*cards[12:15])))
        print("└" + "─" * 32 + "┴" + "─" * 32 + "┴" + "─" * 32 + "┘")

    @staticmethod
    def display_single_item_card(item):
        item_card = item.item_card()
        print('-' * 14, 'Item', '-' * 14)
        print("┌" + "─" * 32 + "┐")
        print("\n".join(f'│ {x} │' for x in item_card))
        print("└" + "─" * 32 + "┘")

    def add_item(self, item):
        """
        adds an item to the party inventory
        :param item:
        :return:
        """

        self.inventory.append(item)

    def equip_gear(self, char, item):
        """
        Equips item in the item.Equip_slot
        :param char: what person to equip
        :param item:  new item to be equipped
        """
        slot = item.equipable_slot
        if char.equip_slots[slot]:
            old_item = char.equip_slots[slot]
            self.inventory.append(old_item)
        char.equip_slots[slot] = item
        if item in self.inventory:
            self.inventory.remove(item)
        char.calculate_stats()

    def change_gold(self, gold_amount):
        #  check if person has enough gold might be better in merchant class
        if self.gold + gold_amount < 0:
            print('Not enough gold!')
            return 'Error'
        self.gold += gold_amount
        return gold_amount

    def sell_equipment(self):
        choice = select_from_list(self.inventory, 'What do you want to sell?', True)

        item_to_sell = self.inventory[choice]
        self.display_single_item_card(item_to_sell)
        question = f'Confirm selling \'{item_to_sell}\' for {item_to_sell.value} gold'
        you_sure = select_from_list(['Yes', 'No'], question, True, True)
        if you_sure == 0:
            self.gold += item_to_sell.value
            self.inventory.remove(item_to_sell)
        else:
            # TODO: Split all menus into callable functions
            pass


if __name__ == '__main__':

    def gen_n_items(n=1):

        for i in range(1, n):
            p1.add_item(Weapon.generate_random())
            p1.add_item(Armor.generate_random())
            i += 1


    p1 = Party.generate()
    gen_n_items(10)
    p1.display_inventory()
