from helper_functions import *
from Hero import *
from person import *
from Equipable_Items import *


class Party:
    def __init__(self, ):
        self.hero = None
        self.members = []
        self.dead_members = []
        # inventory
        self.inventory = []
        self.equipment = []  # used for armor and weapons
        self.gold = 0

    def __str__(self):
        return 'h: ' + str(self.hero()) + ' ' + str(self.members)

    @classmethod
    def generate(cls):
        return cls()

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
    def change_gold(self, gold_amount):
        #  check if person has enough gold might be better in merchant class
        if self.gold + gold_amount < 0:
            print('Not enough gold!')
            return 'Error'
        self.gold += gold_amount
        return gold_amount

    def pickup_gear(self, new_gear):
        """
        entry point
        lets player choose where to put new gear and starts the appropriate methods
        :param new_gear: new item to equip
        :return: -quality='Common'
        """
        #  TODO: display new and old stats to compare (for item type)
        print('You found new equipment!')
        print('------------------------')
        print(new_gear.show_stats())  # TODO: print this
        choices = self.members[:]
        choices.append('equipment')
        print('Where do you want to put it?')
        choice = select_from_list(choices)
        if choice == 'equipment':
            self.equipment.append(new_gear)
        else:
            choice.pickup_gear(new_gear)

    def get_equipment(self, equipped=True):  # , holder=False):
        """
        :param equipped: -> bool: includes equipped items
        # :param holder: -> bool:
        :return: equipment in the party
        """
        equipment = []
        [equipment.append(item) for item in self.equipment]
        if equipped:
            # if holder:
            [[equipment.append(item) for item in member.get_equipped_items()] for member in self.members]
        return equipment

    def get_equpiment_holder_list(self):  # combine with get equipment?
        """
        :return: list of string with item and holder
        """
        equipment_list = self.get_equipment(equipped=True)
        equipment_and_holder_list = []
        for item in equipment_list:
            if item.holder:
                s = str(item) + ', ' + str(item.holder)
            else:
                s = str(item) + ', ' + 'Unused'
            equipment_and_holder_list.append(s)
        return equipment_and_holder_list

    def sell_equipment(self):
        items = self.get_equipment(equipped=True)
        choice = select_from_list(self.get_equpiment_holder_list(), index_pos=True)

        item_to_sell = items[choice]
        self.gold += item_to_sell.value
        print('You sold', item_to_sell, 'for', item_to_sell.value, 'gold')
        if item_to_sell.holder:
            # uneqip item
            pass

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
                self.inventory[item].sell()
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
                 + (9 - len(self.inventory)) * [None]]
        print('\n' * 20)
        print('=' * 41, 'Party Inventory', '=' * 42)
        print("┌" + "─" * 32 + "┬" + "─" * 32 + "┬" + "─" * 32 + "┐")
        print("\n".join(f'│ {x} │ {y} │ {z} │' for x, y, z in zip(*cards[:3])))
        print("├" + "─" * 32 + "┼" + "─" * 32 + "┼" + "─" * 32 + "┤")
        print("\n".join(f'│ {x} │ {y} │ {z} │' for x, y, z in zip(*cards[3:6])))
        print("├" + "─" * 32 + "┼" + "─" * 32 + "┼" + "─" * 32 + "┤")
        print("\n".join(f'│ {x} │ {y} │ {z} │' for x, y, z in zip(*cards[6:9])))
        print("└" + "─" * 32 + "┴" + "─" * 32 + "┴" + "─" * 32 + "┘")

    def display_single_item_card(self, item):
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
            self.inventory.remove(self.inventory.index(item))
        char.calculate_stats()


if __name__ == '__main__':

    def gen_n_items(n=1):

        for i in range(1, n):
            p1.add_item(Weapon.generate_random())
            p1.add_item(Armor.generate_random())
            i += 1


    p1 = Party.generate()
    gen_n_items(10)
    p1.display_inventory()
