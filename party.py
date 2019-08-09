from helper_functions import select_from_list
from Hero import *
from person import *


class Party:
    def __init__(self, ):
        self.hero = None
        self.members = []
        self.dead_members = []
        # inventory
        self.inventory = []
        self.equipment = []  # used for armor and weapons
        self.gold = 0

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
        for member in self.members:
            if not member.is_alive:
                continue
            else:
                return False
        return True

    def kill_everyone(self):
        delete_index = []
        for i, member in enumerate(self.members):
            delete_index.append(i)
        for i in reversed(delete_index):
            self.dead_members.append(self.members.pop(i))

    def party_members_info(self):
        print('=' * 6, 'Party Members Info', '=' * 6)
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
        return any([member.is_hero for member in self.members])

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

    def add_member(self, member):
        """
        adds a member to the party
        :param member: Person or Hero class object
        :return:
        """

        print(f'{member.name}, the {member.profession} joins the party!')
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
        :return: -
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
