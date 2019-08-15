from helper_functions import select_from_list
from Item_Bases import *
from vfx import *
from attack_setups import weapon_setups
from combat_funcs import deal_multi_dmg


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
        self.next_level = 20
        self.worth_xp = 5

        # Base Stats Section!
        self.base_str = 4
        self.base_dex = 4
        self.base_int = 4
        self.base_max_hp = (self.base_str * 5) + (self.level * 5)
        self.base_defense = 0
        self.base_att_dmg_min = 1
        self.base_att_dmg_max = 3
        self.base_crit_chance = 5
        self.base_crit_muliplier = 120

        # Stats Section
        self.str = self.base_str
        self.dex = self.base_dex
        self.int = self.base_int
        self.max_hp = self.base_max_hp + (self.str * 5 // 2) + (self.level * 5)

        self.defense = self.base_defense
        self.att_dmg_min = self.base_att_dmg_min
        self.att_dmg_max = self.base_att_dmg_max
        self.crit_chance = self.base_crit_chance + round(self.dex * 0.8)
        self.crit_muliplier = self.base_crit_muliplier + self.dex

        self.damage = random.randint(self.att_dmg_min, self.att_dmg_max)

        self.hp = self.max_hp

        # Inventory Section
        self.inventory = []
        self.money = money

        self.equip_slots = {'Main Hand': Weapon.generate(quality='Common', quality_val=1, etype='Weapon',
                                                         equipable_slot='Main Hand',
                                                         att_dmg_min=1, att_dmg_max=3),
                            'Off Hand': None,
                            'Head': None,
                            'Chest': None,
                            'Legs': None,
                            'Feet': None,
                            'Ring': None,
                            'Necklace': None,
                            }
        # Calculate stats and gear
        self.stat_growth()
        self.calculate_stats()

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
                              'Leo', 'Phylis', 'Lindsay', 'Tongo', 'Paku', ])
        profession = random.choice(['Warrior', 'Archer', 'Mage', 'Blacksmith', 'Thief', 'Bard'])
        if name == 'Minky':
            profession = 'Miffy Muffin'
        if name == 'Colin':
            profession = 'Bard of Bass'
        return cls(name, profession, level)

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def hp_bar(self, length=10, f_color=bcolors.OKGREEN, m_color=bcolors.FAIL,
               f_char='♥', m_char='-', no_color=False, border='|'):
        '''
        returns a string of an hp_bar for current hp / max hp

        :param border: added at the beginning and the ned of the string
        :param no_color: bool: removes special chars for colors
        :param length: int: length of the bar without border - number of chars
        :param f_color: color code : for filled ticks
        :param m_color: color code : for missing ticks
        :param f_char: str: char to display for filled ticks
        :param m_char: str: char to be displayed for not filled ticks
        :return: hp bar as string
        '''
        bar = BarGFX(self.hp, self.max_hp, length=length, f_color=f_color,
                     m_color=m_color, f_char=f_char, m_char=m_char)
        return bar.bar_str(no_color=no_color, border=border)

    def xp_bar(self, length=10, f_color=bcolors.OKBLUE, m_color=bcolors.OKGREEN,
               f_char='|', m_char='-', no_color=True, border=''):
        '''
        returns a string of an xp_bar for current xp / next_level

        :param border: added at the beginning and the ned of the string
        :param no_color: bool: removes special chars for colors
        :param length: int: length of the bar without border - number of chars
        :param f_color: color code : for filled ticks
        :param m_color: color code : for missing ticks
        :param f_char: str: char to display for filled ticks
        :param m_char: str: char to be displayed for not filled ticks
        :return: xp bar as string
        '''
        bar = BarGFX(self.xp, self.next_level, length=length, f_color=f_color,
                     m_color=m_color, f_char=f_char, m_char=m_char)
        return bar.bar_str(no_color=no_color, border=border)

    def stat_growth(self):
        self.base_str += 1
        self.base_dex += 1
        self.base_int += 1
        if self.profession.lower() == 'warrior':
            self.base_str += 2
            self.base_int -= 1
        elif self.profession.lower() == 'archer':
            self.base_dex += 2
        elif self.profession.lower() == 'mage':
            self.base_int += 2
            self.base_str -= 1

        elif self.profession.lower() == 'thief':
            self.base_int += 1
            self.base_dex += 1
        elif self.profession.lower() == 'blacksmith':
            self.base_str += 1
            self.base_dex += 1
        elif self.profession.lower() == 'bard':
            self.base_str += 1
            self.base_int += 1
        self.calculate_stats()

    def calculate_stats(self):
        self.str = self.base_str
        self.dex = self.base_dex
        self.int = self.base_int
        self.max_hp = self.base_max_hp + (self.str * 5 // 2) + (self.level * 5)
        self.hp = self.max_hp
        self.defense = self.base_defense
        self.att_dmg_min = self.base_att_dmg_min
        self.att_dmg_max = self.base_att_dmg_max
        self.crit_chance = self.base_crit_chance + round(self.dex * 0.8)
        self.crit_muliplier = self.base_crit_muliplier + self.dex
        self.calculate_stats_with_gear()

    def display(self):
        return self.name + ', the ' + self.profession

    def __repr__(self):
        max_left = max(len(k) for k in self.__dict__.keys()) + 10
        return '\n'.join(
            [f"{k.title()}: {str(v).rjust(max_left - len(k), ' ')}"
             for k, v in self.__dict__.items() if v and k[0] != '_'])

    def __str__(self):
        return f'{self.name}, the {self.profession}'

    def info_card(self):

        name = f'{self.name}'
        prof = f'{self.profession}'

        hp = f'HP: {self.hp:>3}/{self.max_hp:<3}'  # 10
        defense = f'Def: {self.defense}'  # 8

        lvl = f'Lvl: {self.level}'
        xp = f'XP: {self.xp}/{self.next_level}'

        stats_str = f'Str: {self.str}'  # Trying 3 probly 2
        stats_dex = f'Dex: {self.dex}'
        stats_int = f'Int: {self.int}'

        dmg_w = 'DMG: '
        dmg_stat = f'{self.att_dmg_min}/{self.att_dmg_max}'  # 11
        crit_w = f'Crit %: '
        crit_stat = f'{self.crit_chance:>2}/{self.crit_muliplier:<3}'  # 15

        # Combine L an R lines
        name = f'{name:<1}{prof:>{21 - len(name)}}'
        level_xp = f'{lvl}{xp:>{21 - len(lvl)}}'
        hp_def = f'{hp}{defense:>{21 - len(hp)}}'
        stats = f'{stats_str:<7}{stats_dex:<7}{stats_int:<7}'
        dmg = f'{dmg_w}{dmg_stat:>{21 - len(dmg_w)}}'
        crit = f'{crit_w}{crit_stat:>{21 - len(crit_w)}}'
        return [name, level_xp, hp_def, stats, dmg, crit]

    def show_stats(self):
        print(f'\n{self.name},the {self.profession}\n'
              f'Level:\t{self.level:>4}  XP: {self.xp:>6}/{self.next_level}\n'
              f'HP:\t   {self.hp}/{self.max_hp:<4}\n'
              f'Str:\t   {self.str:<3}Damage: {self.att_dmg_min:>3}/{self.att_dmg_max:<3}\n'
              f'Dex:\t   {self.dex:<3}Crit:  {self.crit_chance}%/{self.crit_muliplier}%\n'
              f'Int:\t   {self.int:<3}Defence: {self.defense:>5}\n')

    def show_combat_stats(self):
        name = f'{self.name}, the {self.profession}'
        hp = f'Hp: {self.hp:>2}/{self.max_hp:<2}'
        dmg = f'Dmg: {self.att_dmg_min:>2}/{self.att_dmg_max:<2}'
        return f'{name:^23} ' \
            f'{hp:<8} ' \
            f'{dmg:<13}'

    def add_xp(self, xp):
        self.xp += xp
        print(f'{self.name} gained {xp} xp!')
        if self.xp > self.next_level:
            self.level_up()

    def level_up(self):

        self.level += 1
        self.xp -= self.next_level
        self.next_level = round(4 * (self.level ** 3) / 5) + 20
        print(f'{self.name} is now {self.level}!')
        self.stat_growth()

    # stats

    def take_dmg_OBSOLETE(self, amount, dmg_type='physical') -> int:
        """
        reduces person hp by dmg_amount
        :param: amount: int
        :return: actual_dmg: int
        """
        if dmg_type == 'true':
            dmg_multi = 1
        elif dmg_type == 'magic':
            # TODO: implement magic resi
            dmg_multi = amount / (amount + (self.int / 4))
        else:
            dmg_multi = amount / (amount + self.defense)
        actual_dmg = round(amount * dmg_multi)
        self.hp -= actual_dmg
        return actual_dmg

    def take_damage(self, amount):
        """
        reduces person hp by amount
        :param: amount: int
        """
        self.hp -= amount



    def heal(self, amount) -> int:
        """
        heals self for amount
        :param amount: int
        :return: amount healed for: int
        """
        # TODO: is only hotfixed! needs to move to deal_multi_dmg
        amount, is_crit = amount
        self.hp += amount
        if self.hp > self.max_hp:
            healed_amount = self.max_hp - self.hp
            self.hp = self.max_hp
            print(f'{self.name} is fully Healed! HP: {self.hp}/{self.max_hp}')
        else:
            healed_amount = amount
            print(f'{self.name} healed for {amount} hp! HP: {self.hp}/{self.max_hp}')
        return healed_amount

    # Gear and Stat Calculations
    def get_equipped_items(self):
        """
        :return: list of currently equipped items
        """
        return [value for value in self.equip_slots.values() if value]

    def calculate_stats_with_gear(self):
        """
        updates playerstats based on equipped items
        :return: -
        """
        stats = {
            'str': self.str,
            'dex': self.dex,
            'int': self.int,
            'max_hp': self.max_hp,
            'defense': self.defense,
            'att_dmg_min': self.att_dmg_min,
            'att_dmg_max': self.att_dmg_max,
            'crit_chance': self.crit_chance,
            'crit_muliplier': self.crit_muliplier,
        }
        gear = [value for value in self.equip_slots.values() if value]
        for key in stats.keys():
            self.__dict__[key] = stats[key] + sum([item.__dict__[key] for item in gear])

    def show_gear(self):
        items = [self.equip_slot['Main Hand'],
                 self.equip_slot['Off Hand'],
                 self.equip_slot['Head'],
                 self.equip_slot['Chest'],
                 self.equip_slot['Legs'],
                 self.equip_slot['Feet'],
                 self.equip_slot['Ring'],
                 self.equip_slot['Necklace']]
        gear = [item for item in items if item]
        for i in gear:
            print(i.item)

    # def change_gear(self):
    #     if len(self.party.equipment) > 0:
    #         print('What item do you want to equip?')
    #         chosen_gear = select_from_list(self.party.equipment)
    #         self.equip_gear(chosen_gear)
    #         self.party.equipment.remove(chosen_gear)
    #
    # def pickup_gear(self, new_gear):
    #     """
    #     ENDPOINT to get new items to the player
    #     :param new_gear: a new item
    #     :return:
    #     """
    #     if new_gear.gear_type == 'weapon':
    #         if self.equip_slot['Main Hand']:
    #             print('-----------------------')
    #             print('Current First Hand Weapon:')
    #             self.equip_slot['Main Hand'].show_stats()
    #         else:
    #             self.equip_gear(new_gear)
    #             return
    #         if self.equip_slot['Off Hand']:
    #             print('-----------------------')
    #             print('Current Off Hand Weapon:')
    #             self.equip_slot['Off Hand'].show_stats()
    #     self.equip_gear(new_gear)
    #
    # def equip_gear(self, new_gear, slot_to_change='choose'):
    #     """
    #     changes/fills an item in an equipment slot
    #     puts old item into party inventory
    #     :param slot_to_change: provide if you want to auto equip
    #     :param new_gear:  new item to be equipped
    #     :return: -
    #     """
    #     if slot_to_change == 'choose':
    #         if new_gear.gear_type == 'weapon':
    #             print('Where do you want to put it?')
    #             weapon_slot = select_from_list(['Main Hand', 'Off Hand'], index_pos=True)
    #             if weapon_slot == 0:
    #                 slot_to_change = 'main_hand'
    #             elif weapon_slot == 1:
    #                 slot_to_change = 'off_hand'
    #         elif new_gear.gear_type == 'shield':
    #             slot_to_change = 'off_hand'
    #         # TODO: add elifs for all equipment slots
    #         elif new_gear.gear_type == 'armor':
    #             slot_to_change = 'armor'
    #
    #     if self.__dict__[slot_to_change]:
    #         old_item = self.__dict__[slot_to_change]
    #         old_item.holder = None
    #         self.party.equipment.append(old_item)
    #     #  TODO: check and ask if switch weapon in slot
    #     self.__dict__[slot_to_change] = new_gear
    #     new_gear.holder = self
    #     self.calculate_stats_with_gear()

    # battle

    def calculate_dmg(self, dmg_type='physical', can_crit=True):
        """
        generates dmg
        determines hit is critical
        :return: dmg int
        """
        is_crit = False
        # TODO: how calc true dmg?
        if dmg_type == 'magic':
            dmg = self.int
        else:  # if dmg_type == 'physical':
            dmg = random.randint(self.att_dmg_min, self.att_dmg_max)
        if can_crit:
            if random.randrange(100) < self.crit_chance:
                is_crit = True
                dmg = (dmg * self.crit_muliplier) // 100

        return dmg, is_crit

    #  TODO: refactor combat functions to Combat.py
    def deal_dmg(self, target) -> int:
        """
        generates dmg and lets target take dmg
        :param target: person instance
        :return: actual dmg dealt -> int
        """
        dmg_dealt = self.calculate_dmg()
        dmg_enemy_received = target.take_dmg(dmg_dealt)
        # print(self, 'deals', dmg_enemy_received, 'to', target)
        return dmg_enemy_received

    def choose_target(self, target_party):
        """
        picks random target from target_party.members
        :param target_party: party instance
        :return: person from party
        """
        if len(target_party) > 1:
            if self.party.has_hero() or self.party.game.difficulty == 'Medium':
                choice = random.randrange(len(target_party))
                target = target_party[choice]
            else:
                if self.party.game.difficulty == 'Hard':
                    target = min(target_party, key=lambda member: member.hp)
                elif self.party.game.difficulty == 'Easy':
                    target = max(target_party, key=lambda member: member.hp)
        else:
            target = target_party[0]
        return target

    def choose_attack(self):
        choice = random.choice(self.get_attack_options())
        return choice

    def attack(self, target_party, mode='single attack'):
        """
        chooses deal_dmg func, based on mode
        executes chosen deal_dmg
        :param target_party: party instance
        :param mode: str
        :return:
        """
        # TODO: make this independent of setup file! (get the setup from the weapon)
        setup_key = self.choose_attack()
        setup = weapon_setups[setup_key]
        dmg_done = deal_multi_dmg(self, target_party, **setup)
        # target = self.choose_target(target_party)
        # mode = self.choose_attack().lower()
        # if mode == 'single attack':
        #     dmg_done = self.deal_dmg(target)
        # elif mode == 'multi attack':
        #     dmg_done = self.deal_multi_dmg(target, target_num='all', splash_dmg=75, primary=False)
        # elif mode == 'multi attack with primary target':
        #     dmg_done = self.deal_multi_dmg(target, target_num=2, splash_dmg=50)
        return dmg_done

    def choose_battle_action(self, enemy_party):
        """
        ENDPOINT for battle
        npc will always choose basic attack
        :param enemy_party:
        :return: -
        """
        possible_actions = ['attack', ]
        if self.party.game.difficulty == 'Medium':
            heal_under = 0.2
        elif self.party.game.difficulty == 'Hard':
            heal_under = 0.3
        else:
            heal_under = 0.05
        if self.hp / self.max_hp < heal_under:
            possible_actions.append('heal')
        action = random.choice(possible_actions)
        return action

    def get_attack_options(self):
        # TODO: make a list of options based on <???>
        # return ['single attack', 'multi attack', 'multi attack with primary target']  # full list disabled for now
        return [item.attack_name for item in [self.equip_slots['Main Hand'], self.equip_slots['Off Hand']] if item]
        # return ['single attack']

    def battle_turn(self, enemy_party):
        action = self.choose_battle_action(enemy_party).lower()
        if action == 'attack':
            dmg_done = self.attack(enemy_party)
            # target = self.choose_target(enemy_party)
            # # TODO: refactor to input chosen target, not party
            # # self.attack_target(target, mode=action)  # not needed until we have more options to do dmg
            # dmg_enemy_received = self.deal_dmg(target)
            # print(self.name, 'deals', dmg_enemy_received, 'to', target.name)

        elif action == 'show hero stats':
            self.party.display_single_member_item_card(self)
            self.battle_turn(enemy_party)
        elif action == 'change gear':
            # self.change_gear()
            self.battle_turn(enemy_party)
        elif action == 'heal':
            self.heal(self.calculate_dmg())

    def deal_multi_dmg(self, target, target_num='all', splash_dmg=25, primary=True, rnd_target=True):
        if target_num == 'all' or target_num > len(target.party.members):
            target_num = len(target.party.members)

        members_list = target.party.members[:]
        dmg_received = 0

        if primary:
            dmg_dealt = self.calculate_dmg()
            dmg_received += target.take_dmg(dmg_dealt)
            print(self.display(), 'deals', dmg_received, 'dmg to', target.display())
            members_list.remove(target)
            target_num -= 1

        while target_num > 0:
            if rnd_target:
                target = random.choice(members_list)
            elif target_num < len(members_list):
                target = select_from_list(members_list, q='Select next target')
            else:
                target = members_list[0]
            dmg_received2 = target.take_dmg(self.calculate_dmg() * splash_dmg // 100)
            print('and', dmg_received2, 'dmg to', target)
            dmg_received += dmg_received2
            members_list.remove(target)
            target_num -= 1
        return dmg_received


if __name__ == '__main__':
    p1 = Person.generate_random()
