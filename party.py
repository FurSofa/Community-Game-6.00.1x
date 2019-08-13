from helper_functions import *
# from Hero import *
# from person import *
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
        x = select_from_list(['Inventory', 'Character Inventory', 'exit'], True)
        if x == '0':
            self.display_inventory()
            selection = select_from_list(['', '', '', ''], True)
        if x == '1':
            pass
        if x == '2':
            pass

    def display_inventory(self):
        pass

    def print_inventory(self):
        empty_card = [" " * 30] * 3
        cards = [item.item_card() if item else empty_card for item in self.inventory
                 + (9 - len(self.inventory)) * [None]]
        print("┌" + "─" * 32 + "┬" + "─" * 32 + "┬" + "─" * 32 + "┐")
        print("\n".join(f'│ {x} │ {y} │ {z} │' for x, y, z in zip(*cards[:3])))
        print("├" + "─" * 32 + "┼" + "─" * 32 + "┼" + "─" * 32 + "┤")
        print("\n".join(f'│ {x} │ {y} │ {z} │' for x, y, z in zip(*cards[3:6])))
        print("├" + "─" * 32 + "┼" + "─" * 32 + "┼" + "─" * 32 + "┤")
        print("\n".join(f'│ {x} │ {y} │ {z} │' for x, y, z in zip(*cards[6:])))
        print("└" + "─" * 32 + "┴" + "─" * 32 + "┴" + "─" * 32 + "┘")

    def add_item(self, item):
        self.inventory.append(item)

    def show_gear(self, inventory):

        for i in inventory:
            if i:
                print(i.show_stats())
            else:
                print('empty')

    def equip_gear(self, new_gear, slot_to_change='choose'):
        """
        changes/fills an item in an equipment slot
        puts old item into party inventory
        :param slot_to_change: provide if you want to auto equip
        :param new_gear:  new item to be equipped
        :return: -
        """
        if slot_to_change == 'choose':
            if new_gear.gear_type == 'weapon':
                print('Where do you want to put it?')
                weapon_slot = select_from_list(['Main Hand', 'Off Hand'], index_pos=True)
                if weapon_slot == 0:
                    slot_to_change = 'main_hand'
                elif weapon_slot == 1:
                    slot_to_change = 'off_hand'
            elif new_gear.gear_type == 'shield':
                slot_to_change = 'off_hand'
            # TODO: add elifs for all equipment slots
            elif new_gear.gear_type == 'armor':
                slot_to_change = 'armor'

        if self.__dict__[slot_to_change]:
            old_item = self.__dict__[slot_to_change]
            old_item.holder = None
            self.party.equipment.append(old_item)
        #  TODO: check and ask if switch weapon in slot
        self.__dict__[slot_to_change] = new_gear
        new_gear.holder = self
        self.calculate_stats_with_gear()

# if __name__ == '__main__':
#
#     def gen_n_items(n=1):
#
#         for i in range(1,n):
#             p1.add_item(Weapon.generate_random())
#             p1.add_item(Armor.generate_random())
#             i += 1
#
#     p1 = Party.generate()
#     gen_n_items(5)
#     p1.show_gear(p1.inventory)
