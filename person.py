import random
from helper_functions import select_from_list
import random
import Equipable_Items


class Person:
    """
    access points:
    pickup_gear() to give the player a new weapon
    choose_battle_action() to start a battle turn (choosing actions and executing the appropriate methods)
    """

    def __init__(self, name='Mr. Lazy', profession='warrior', level=1, money=25):
        """
        Create new person """

        self.hero = False
        self.name = name
        self.profession = profession
        self.party = None  # Only one party at a time

        self.level = level
        self.xp = 0
        self.xp_to_lvl_up = 20

        # Base Stats Section!
        self.base_str = 5 + random.randint(0, 2)
        self.base_dex = 5 + random.randint(0, 2)
        self.base_int = 5 + random.randint(0, 2)
        self.base_max_hp = 30 + (self.base_str * 5) + (self.level * 5)
        self.base_defense = 1
        self.base_att_dmg_min = 1
        self.base_att_dmg_max = 4
        self.base_damage = random.randint(self.base_att_dmg_min,
                                          self.base_att_dmg_max) \
                           + int((self.base_dex * 3) // 3)
        self.base_crit_chance = 5
        self.base_crit_muliplier = 150

        # Stats Section
        self.str = self.base_str
        self.dex = self.base_dex
        self.int = self.base_int
        self.max_hp = self.base_max_hp
        self.defense = self.base_defense
        self.att_dmg_min = self.base_att_dmg_min
        self.att_dmg_max = self.base_att_dmg_max

        # TODO: one static value or a range for damage?
        self.damage = random.randint(self.att_dmg_min, self.att_dmg_max) \
                      + int((self.dex + self.str) // 2)
        self.crit_chance = self.base_crit_chance
        self.crit_muliplier = self.base_crit_muliplier

        self.max_hp = self.base_max_hp
        self.hp = self.max_hp
        self.profession_stat_augment()

        # Inventory Section
        self.inventory = []
        self.money = money

        # weapons
        self.main_hand = None
        self.off_hand = None

        # armor
        self.head = None
        self.chest = None
        self.legs = None
        self.feet = None

        # accessories
        self.ring = None
        self.necklace = None
        self.relevant_gear = [self.main_hand,
                              self.off_hand,
                              self.head,
                              self.chest,
                              self.legs,
                              self.feet,
                              self.ring,
                              self.necklace]

    @classmethod
    def generate(cls, name='Jeb', profession='Warrior', level=1):
        """
        Create new character at level 1
        """
        return cls(name, profession, level)

    @classmethod
    def generate_random(cls, level=1):
        """
        Create new random character at level 1
        """
        level = level
        name = random.choice(['Lamar', 'Colin', 'Ali', 'Jackson', 'Minky',
                              'Leo', 'Lilli', 'Lindsay', 'Tongo', 'Paku', ])
        profession = random.choice(['Warrior', 'Archer', 'Mage', 'Farmer', 'Blacksmith'])
        if name == 'Minky':
            profession = 'Miffy Muffin'
        if name == 'Colin':
            profession = 'Bass Bard'
        return cls(name, profession, level)

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def test_equip(self):
        self.main_hand = Equipable_Items.create_random_equipable_item(1, 1)
        self.off_hand = Equipable_Items.create_random_equipable_item(1, 1)
        self.head = Equipable_Items.create_random_equipable_item(1, 2)

    def profession_stat_augment(self):
        if self.profession == 'Warrior':
            self.str += random.randint(0, 3)
            self.dex += random.randint(0, 1)
            self.int -= random.randint(0, 3)
            self.xp_to_lvl_up -= (self.int * 2 // 4)

        elif self.profession == 'Archer':
            self.str += random.randint(0, 1)
            self.dex += random.randint(0, 3)
            self.int += random.randint(0, 1)
            self.xp_to_lvl_up -= (self.int * 3 // 3)

        elif self.profession == 'Mage':
            self.str -= random.randint(0, 3)
            self.dex += random.randint(0, 1)
            self.int += random.randint(0, 3)
            self.xp_to_lvl_up -= (self.int * 4 // 2)

    def __repr__(self):
        max_left = max(len(k) for k in self.__dict__.keys()) + 10
        return '\n'.join(
            [f"{k.title()}: {str(v).rjust(max_left - len(k), ' ')}"
             for k, v in self.__dict__.items() if v and k[0] != '_'])

    def __str__(self):
        return f'\n{self.name},the {self.profession}\n' \
            f'Level:\t{self.level:>4}  XP: {self.xp:>6}/{self.xp_to_lvl_up}\n' \
            f'HP:\t   {self.hp}/{self.max_hp:<4}\n' \
            f'Str:\t   {self.str:<3}Damage: {self.damage:>6}\n' \
            f'Dex:\t   {self.dex:<3}Crit:  {self.crit_chance}%/{self.crit_muliplier}%\n' \
            f'Int:\t   {self.int:<3}Defence: {self.defense:>5}\n'

    def show_stats(self):
        print(f'\n{self.name},the {self.profession}\n'
              f'Level:\t{self.level:>4}  XP: {self.xp:>6}/{self.xp_to_lvl_up}\n'
              f'HP:\t   {self.hp}/{self.max_hp:<4}\n'
              f'Str:\t   {self.str:<3}Damage: {self.damage:>6}\n'
              f'Dex:\t   {self.dex:<3}Crit:  {self.crit_chance}%/{self.crit_muliplier}%\n'
              f'Int:\t   {self.int:<3}Defence: {self.defense:>5}\n')

    def show_combat_stats(self):
        name = f'{self.name}, the {self.profession}'
        hp = f'Hp: {self.hp:>2}/{self.max_hp:<2}'
        dmg = f'Dmg: {self.att_dmg_min:>2}/{self.att_dmg_min:<2}'
        return f'- {name:^23} ' \
            f'{hp:<8} ' \
            f'{dmg:<13}'

    def show_stats_old(self):
        """
        Prints out Stats for the person
        """
        relevant_stats = {
            '\nName': self.name,
            'Max HP': self.max_hp,
            'HP': self.hp,
            'Attack Damage': self.damage,
            'Defense': self.defense,
            'Crit Chance %': self.crit_chance,
            'Crit Damage %': self.crit_muliplier
        }
        for k, v in relevant_stats.items():
            print(k, ': ', v)

    # stats

    def take_dmg(self, amount) -> int:
        """
        reduces person hp by dmg_amount
        :param: amount: int
        :return: actual_dmg: int
        """
        dmg_multi = amount / (amount + self.defense)
        actual_dmg = round(amount * dmg_multi)
        self.hp -= actual_dmg
        print(f'{self.name} took {actual_dmg} damage out of {amount} received.')
        return actual_dmg

    def heal(self, amount) -> int:
        """
        heals self for amount
        :param amount: int
        :return: amount healed for: int
        """
        self.hp += amount
        if self.hp > self.max_hp:
            healed_amount = self.max_hp - self.hp
            self.hp = self.max_hp
            print(f'{self.name} is fully Healed! HP: {self.hp}/{self.max_hp}\n')
        else:
            healed_amount = amount
            print(f'{self.name} healed for {amount} hp! HP: {self.hp}/{self.max_hp}\n')
        return healed_amount

    # Gear and Stat Calculations
    def get_equipped_items(self):
        """
        :return: list of currently by the player equipped items
        """
        items = [self.main_hand,
                 self.off_hand,
                 self.chest,
                 self.legs,
                 self.feet,
                 self.ring,
                 self.necklace]
        return [item for item in items if item]

    def calculate_stats_with_gear(self):
        """
        updates playerstats based on equipped items
        :return: -
        """
        stats = {
            'str': self.base_str,
            'dex': self.base_dex,
            'int': self.base_int,
            'max_hp': self.base_max_hp,
            'defense': self.base_defense,
            'att_dmg_min': self.base_att_dmg_min,
            'att_dmg_max': self.base_att_dmg_max,
            'crit_chance': self.base_crit_chance,
            'crit_muliplier': self.base_crit_muliplier,
        }
        gear = self.get_equipped_items()
        for key in stats.keys():
            self.__dict__[key] = stats[key] + sum([item.__dict__[key] for item in gear])

        # TODO: range or static dmg?
        # self.current_crit_dmg = int(self.current_attack_dmg * (self.current_crit_modifier / 100))

    #  manage gear
    def change_gear(self):
        if len(self.party.equipment) > 0:
            print('What item do you want to equip?')
            chosen_gear = select_from_list(self.party.equipment)
            self.equip_gear(chosen_gear)
            self.party.equipment.remove(chosen_gear)

    def pickup_gear(self, new_gear):
        """
        ENDPOINT to get new items to the player
        :param new_gear: a new item
        :return:
        """
        if new_gear.gear_type == 'weapon':
            if self.main_hand:
                print('-----------------------')
                print('Current First Hand Weapon:')
                self.main_hand.show_stats()
            else:
                self.equip_gear(new_gear)
                return
            if self.off_hand:
                print('-----------------------')
                print('Current Off Hand Weapon:')
                self.off_hand.show_stats()
        self.equip_gear(new_gear)

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

    # battle

    def calculate_dmg(self) -> int:
        """
        generates dmg
        determines hit is critical
        :return: dmg int
        """
        dmg = self.damage
        if random.randrange(100) < self.crit_chance:
            dmg = (dmg * self.crit_muliplier) // 100
            # print(f'{self.name} lands a critical strike dealing {dmg} damage!')
        return dmg

    #  TODO: refactor combat functions to Combat.py
    def deal_dmg(self, target) -> int:
        """
        generates dmg and lets target take dmg
        :param target: person instance
        :return: actual dmg dealt -> int
        """
        dmg_dealt = self.calculate_dmg()
        dmg_enemy_received = target.take_dmg(dmg_dealt)
        print(self, 'deals', dmg_enemy_received, 'to', target)
        return dmg_enemy_received

    def choose_target(self, target_party):
        """
        picks random target from target_party.members
        :param target_party: party instance
        :return: person from party
        """
        if len(target_party.members) > 1:
            choice = random.randrange(len(target_party.members) - 1)
        else:
            choice = 0
        return target_party.members[choice]

    #  TODO: maybe split up into smaller parts
    def attack_target(self, target_party, mode='basic attack'):
        """
        chooses deal_dmg func, based on mode
        executes chosen deal_dmg
        :param target_party: party instance
        :param mode: str
        :return:
        """
        physical_attack_modes = ['basic attack', 'main weapon attack', 'off hand weapon attack']
        if mode in physical_attack_modes:
            target = self.choose_target(target_party)
            print('target:', target)
            if mode == 'basic attack':
                dmg_enemy_received = self.deal_dmg(target)
            elif mode == 'main weapon attack':
                dmg_enemy_received = self.main_hand.deal_dmg(target)
            elif mode == 'off hand weapon attack':
                dmg_enemy_received = self.off_hand.deal_dmg(target)
            print(target.show_combat_stats())

    def choose_battle_action(self, enemy_party):
        """
        ENDPOINT for battle
        npc will always choose basic attack
        :param enemy_party:
        :return: -
        """
        possible_actions = ['basic attack', 'main weapon attack']
        action = 'basic attack'
        self.attack_target(enemy_party, mode=action)
