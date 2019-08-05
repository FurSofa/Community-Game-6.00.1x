import random
from helper_functions import player_choose_from_list
from weapons import *
import random


class Person:
    """
    access points:
    pickup_gear() to give the player a new weapon
    choose_battle_action() to start a battle turn (choosing actions and executing the appropriate methods)
    """

    def __init__(self, name='Mr. Lazy', profession='Warrior', level=1, money=25):
        """
        Create new person """

        self.name = name
        self.profession = profession
        self.party = []

        self.level = level
        self.exp = 0
        self.next_lvl_xp = 20

        self.str = 5 + random.randint(0, 2)
        self.dex = 5 + random.randint(0, 2)
        self.int = 5 + random.randint(0, 2)

        self.max_hp_base = 30 + (self.str * 5) + (self.level * 5)
        self.max_hp = self.max_hp_base
        self.hp = self.max_hp

        self.defense = 1
        self.damage = 5 + int((self.str + self.dex) // 2)

        self.inventory = []
        self.money = money

        # weapons
        self.main_hand = None
        self.off_hand = None

        # armor
        self.chest = None
        self.legs = None
        self.feet = None

        # accessories
        self.ring = None
        self.necklace = None
        self.relevant_gear = [self.main_hand,
                              self.off_hand,
                              self.chest,
                              self.legs,
                              self.feet,
                              self.ring,
                              self.necklace]

        self.not_relevant_stats = ['gear_slot', 'holder']

    @classmethod
    def generate(cls, name='Mr. Lazy', profession='Warrior'):
        return cls(name, profession)

    def profession_stat_augment(self):
        if self.profession == 'Warrior':
            self.str += random.randint(0, 3)
            self.dex += random.randint(0, 1)
            self.int -= random.randint(0, 3)
            self.lvl_up_xp -= int(self.int * 2 // 4)

        elif self.profession == 'Archer':
            self.str += random.randint(0, 1)
            self.dex += random.randint(0, 3)
            self.int += random.randint(0, 1)
            self.lvl_up_xp -= int(self.int * 3 // 3)

        elif self.profession == 'Mage':
            self.str -= random.randint(0, 3)
            self.dex += random.randint(0, 1)
            self.int += random.randint(0, 3)
            self.lvl_up_xp -= int(self.int * 4 // 2)

    def __repr__(self):
        pass

    def __str__(self):
        return str(self.name + ', ' + self.profession)

    def show_stats(self):
        """
        Prints out Stats for the person
        """
        relevant_stats = {
            'Name': self.name,
            'Max HP': self.max_health,
            'HP': self.health,
            'Attack Damage': self.current_attack_dmg,
            'Defense': self.defense,
            'Crit Chance %': self.current_crit_chance,
            'Crit Damage %': self.current_crit_modifier
        }
        for k, v in relevant_stats.items():
            print(k, ': ', v)

    # stats
    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def get_eqipped_items(self):
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
            'max_health': self.max_health,
            'defense': self.base_defense,
            'attack_dmg': self.base_attack_dmg,
            'crit_chance': self.base_crit_chance,
            'crit_modifier': self.base_crit_modifier,
        }
        gear = self.get_eqipped_items()
        for key in stats.keys():
            self.__dict__['current_' + key] = stats[key] + sum([item.__dict__[key] for item in gear])
        self.current_crit_dmg = int(self.current_attack_dmg * (self.current_crit_modifier / 100))

    def calculate_stats_with_gear_old(self):
        combined_gear_stats = {}
        for item in self.get_eqipped_items():
            if item:
                gear_stats = item.__dict__
                for stat in gear_stats.keys():
                    if stat not in self.not_relevant_stats:
                        if stat in combined_gear_stats.keys():
                            combined_gear_stats[stat] = combined_gear_stats[stat] + gear_stats[stat]
                        else:
                            combined_gear_stats[stat] = gear_stats[stat]
        for stat in combined_gear_stats.keys():
            self.__dict__['current_' + stat] = self.__dict__['base_' + stat] + combined_gear_stats[stat]

    #  manage gear
    def change_gear(self):
        if len(self.party.equipment) > 0:
            print('What item do you want to equip?')
            chosen_gear = player_choose_from_list(self.party.equipment)
            self.equip_gear(chosen_gear)
            self.party.equipment.remove(chosen_gear)

    def pickup_gear(self, new_gear):
        """
        ENDPOINT to get new items to the player
        :param new_gear: a new item
        :return:
        """
        #  TODO: display new and old stats to compare (for item type)
        print('You found new equipment!')
        print('-----------------------')
        new_gear.show_stats()
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
        print('-----------------------')
        print('Do you want to equip it now?')
        player_choice = player_choose_from_list(['Put on now', 'Put in inventory'], index_pos=True)
        if player_choice == 0:
            self.equip_gear(new_gear)
        elif player_choice == 1:
            self.party.equipment.append(new_gear)

    def equip_gear(self, new_gear):
        """
        changes/fills an item in an equipment slot
        puts old item into party inventory
        :param new_gear:  new item to be equipped
        :return: -
        """
        if new_gear.gear_type == 'weapon':
            print('Where do you want to put it?')
            weapon_slot = player_choose_from_list(['Main Hand', 'Off Hand'], index_pos=True)
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
    def take_dmg(self, amount) -> int:
        """
        reduces person hp by dmg_amount
        :param dmg_amount: int
        :return: dmg_taken: int
        """
        dmg_taken = amount - self.defense
        if dmg_taken < 0:
            dmg_taken = 0
        self.health -= dmg_taken
        return dmg_taken

    def calculate_dmg(self) -> int:
        """
        generates dmg
        determines hit is critical
        :return: dmg int
        """
        dmg = self.current_attack_dmg
        if random.randrange(100) < self.current_crit_chance:
            dmg = self.current_crit_dmg
            print(self, 'lands a critical strike!')
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
            print(target, 'hp:', target.health)

    def heal(self, amount) -> int:
        """
        heals self for amount
        :param amount: int
        :return: amount healed for: int
        """
        self.health += amount
        if self.health > self.max_health:
            healed_amount = self.max_health - self.health
            self.health = self.max_health
            print(self, 'is fully Healed!')
        else:
            healed_amount = amount
            print(self, 'healed for', amount, 'hp')
        return healed_amount

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


p = Person.generate('tod','Archer')

print(p)
