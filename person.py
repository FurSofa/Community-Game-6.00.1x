import random
from helper_functions import player_choose_from_list
from weapons import *


class Person:
    def __init__(self, name):
        # general stats
        self.name = name
        self.type = 'Base NPC'
        self.party = None

        # defence stats
        self.base_max_health = 20
        self.current_max_health = self.base_max_health
        self.health = self.current_max_health
        self.base_defence = 0
        self.current_defence = self.base_defence

        # damage relevant stats
        self.base_attack_dmg = 5
        self.base_crit_chance = 5
        self.base_crit_dmg = self.base_attack_dmg * 2

        self.current_attack_dmg = self.base_attack_dmg
        self.current_crit_chance = self.base_crit_chance
        self.current_crit_dmg = self.base_crit_dmg

        # weapons
        self.first_hand_weapon = None
        self.off_hand = None

        # gear
        self.chest = None
        self.shoulders = None
        self.legs = None
        self.feet = None

        # accessories
        self.ring = None
        self.necklace = None
        self.stat_relevant_gear = [self.first_hand_weapon, self.off_hand, self.chest, self.shoulders,
                                   self.legs, self.feet, self.ring, self.necklace]
        self.not_relevant_stats = ['gear_slot', 'holder']

    def __str__(self):
        return str(self.name + ', ' + self.type)

# stats
    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def calculate_stats_with_gear(self):
        combined_gear_stats = {}
        for item in self.stat_relevant_gear:
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

    def show_stats(self):
        relevant_stats = {
            'Name': self.name,
            'Max HP': self.current_max_health,
            'HP': self.health,
            'Attack Damage': self.current_attack_dmg,
            'Defense': self.current_defence,
            'Crit Chance': self.current_crit_chance,
            'Crit Damage': self.current_crit_dmg
        }
        for k, v in relevant_stats.items():
            print(k, ': ', v)

#  manage gear
    def change_gear(self):
        if len(self.party.equipment) > 0:
            print('What item do you want to equip?')
            chosen_gear = player_choose_from_list(self.party.equipment)
            self.equip_gear(chosen_gear)
            self.party.equipment.remove(chosen_gear)

    def pickup_gear(self, new_gear):
        #  TODO: display new and old stats to compare (for item type)
        print('You found new equipment!')
        print('-----------------------')
        new_gear.show_stats()
        if new_gear.gear_type == 'weapon':

            if self.first_hand_weapon:
                print('-----------------------')
                print('Current First Hand Weapon:')
                self.first_hand_weapon.show_stats()
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
        if new_gear.gear_type == 'weapon':
            print('Where do you want to put it?')
            weapon_slot = player_choose_from_list(['First hand', 'Off Hand'], index_pos=True)
            if weapon_slot == 0:
                slot_to_change = 'first_hand_weapon'
            elif weapon_slot == 1:
                slot_to_change = 'off_hand'
            #  TODO: check if shield or armor
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
    def take_dmg(self, dmg_amount):
        dmg_taken = dmg_amount - self.current_defence
        if dmg_taken < 0:
            dmg_taken = 0
        self.health -= dmg_taken
        return dmg_taken

    def calculate_dmg(self):
        dmg = self.current_attack_dmg
        if random.randrange(100) < self.current_crit_chance:
            dmg = dmg * self.current_crit_dmg // 100
            print(self, 'lands a critical strike!')
        return dmg

    #  TODO: refactor deal_damage to general function with single and multi target
    def deal_dmg(self, target):
        dmg_dealt = self.calculate_dmg()
        dmg_enemy_received = target.take_dmg(dmg_dealt)
        print(self, 'deals', dmg_enemy_received, 'to', target)
        return dmg_enemy_received

    def choose_target(self, target_party):
        if len(target_party.members) > 1:
            choice = random.randrange(len(target_party.members) - 1)
        else:
            choice = 0
        return target_party.members[choice]

    #  TODO: maybe split up into smaller parts
    def attack_target(self, target_party, mode='basic attack'):
        physical_attack_modes = ['basic attack', 'main weapon attack', 'off hand weapon attack']
        if mode in physical_attack_modes:
            target = self.choose_target(target_party)
            print('target:', target)
            if mode == 'basic attack':
                dmg_enemy_received = self.deal_dmg(target)
            elif mode == 'main weapon attack':
                dmg_enemy_received = self.first_hand_weapon.deal_dmg(target)
            elif mode == 'off hand weapon attack':
                dmg_enemy_received = self.off_hand.deal_dmg(target)
            print(target, 'hp:', target.health)

    def heal(self, amount):
        self.health += amount
        if self.health > self.base_max_health:
            self.health = self.base_max_health
            print(self, 'is fully Healed!')
        else:
            print(self, 'healed for', amount, 'hp')
        return amount

    def choose_battle_action(self, enemy_party):
        possible_actions = ['basic attack', 'main weapon attack']
        action = 'basic attack'
        self.attack_target(enemy_party, mode=action)


class Hero(Person):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'Hero'

        # defence stats
        self.base_max_health = 20
        self.current_max_health = self.base_max_health
        self.health = self.current_max_health
        self.base_defence = 0
        self.current_defence = self.base_defence

        # damage relevant stats
        self.base_attack_dmg = 5
        self.current_attack_dmg = self.base_attack_dmg
        self.crit_chance = 10
        self.crit_dmg = 150

    def choose_target(self, target_party):
        print('Choose a target:')
        return player_choose_from_list(target_party.members)

    def choose_battle_action(self, enemy_party):
        #  TODO: find a place to store possible actions
        possible_actions = ['basic attack', ]
        if self.first_hand_weapon:
            possible_actions.append('main weapon attack')
        if self.off_hand:
            if self.off_hand.gear_type == 'weapon':
                possible_actions.append('off hand weapon attack')
        if len(self.party.equipment) > 0:
            possible_actions.append('change gear')
        #  basic attack
        #  main weapon attack
        #  spell
        #  inventory
        possible_actions.append('Show Hero Stats')
        action = player_choose_from_list(possible_actions)
        if action == 'change gear':
            self.change_gear()
            self.choose_battle_action(enemy_party)
        elif action == 'Show Hero Stats':
            self.show_stats()
            self.choose_battle_action(enemy_party)
        self.attack_target(enemy_party, mode=action)


#  example on how to modify methods
class Vampire(Person):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'Vampire'
        self.base_vampirism = 50
        self.base_defence = 0

    def calc_vamp_heal(self, dealt_dmg):
        return dealt_dmg // (100 // self.base_vampirism)

    def deal_dmg(self, target):
        dealt_dmg = super().deal_dmg(target)
        self.heal(self.calc_vamp_heal(dealt_dmg))
        return dealt_dmg


class Blocker(Person):
    def __init__(self, name):
        super().__init__(name)
        self.defence = 4
        self.type = 'Blocker'
