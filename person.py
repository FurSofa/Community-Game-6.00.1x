import random
from helper_functions import player_choose_from_list


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
        self.current_attack_dmg = self.base_attack_dmg
        self.base_crit_chance = 5
        self.current_crit_chance = self.base_crit_chance
        self.base_crit_dmg = 150
        self.current_crit_dmg = self.base_crit_dmg

        # inventory
        self.weapons = []
        self.inventory = []
        self.equipment = []
        self.gold = 0

    def __repr__(self):
        return self.name + ', ' + self.type

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def calculate_stats_with_weapon(self):
        combined_weapons = {}
        for weapon in self.weapons:
            weapon_stats = weapon.__dict__
            for stat in weapon_stats.keys():
                if stat == 'holder':
                    continue
                if stat in combined_weapons.keys():
                    combined_weapons[stat] = combined_weapons[stat] + weapon_stats[stat]
                else:
                    combined_weapons[stat] = weapon_stats[stat]
        for stat in combined_weapons.keys():
            self.__dict__['current_'+stat] = self.__dict__['base_'+stat] + combined_weapons[stat]

#  inventory and trading
    def change_gold(self, gold_amount):
        #  check if person has enough gold might be better in merchant class
        if self.gold + gold_amount < 0:
            print('Not enough gold!')
            return 'Error'
        self.gold += gold_amount
        return gold_amount

    def equip_weapon(self, new_weapon):
        self.weapons.append(new_weapon)
        new_weapon.holder = self
        self.calculate_stats_with_weapon()



# battle relevant methods
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
            print(self, 'lands a critical strik!')
        return dmg

    def deal_dmg(self, target):
        dmg_dealt = self.calculate_dmg()
        dmg_enemy_received = target.take_dmg(dmg_dealt)
        print(self, 'deals', dmg_enemy_received, 'to', target)
        return dmg_enemy_received

    #  TODO: check if needed, maybe refactor
    def use_weapon_attack(self, target):
        dmg_received = self.weapons[0].deal_dmg(target)

    def choose_target(self, target_party):
        if len(target_party.members) > 1:
            choice = random.randrange(len(target_party.members)-1)
        else:
            choice = 0
        return target_party.members[choice]

    #  TODO: maybe split up into smaller parts
    def attack_target(self, target_party, mode='basic attack'):
        if mode == 'basic attack' or mode == 'weapon special attack':
            target = self.choose_target(target_party)
            print('target:', target)
            if mode == 'weapon special attack':
                dmg_enemy_received = self.weapons[0].deal_dmg(target)
            elif mode == 'basic attack':
                dmg_enemy_received = self.deal_dmg(target)
            print(target, 'hp:', target.health)

    def heal(self, amount):
        self.health += amount
        if self.health > self.base_max_health:
            self.health = self.base_max_health
            print(self, 'is fully Healed!')
        else:
            print(self, 'healed for', amount, 'hp')
        return amount

    def choose_action(self, enemy_party):
        possible_actions = ['basic attack', 'weapon special attack']
        action = 'basic attack'
        self.attack_target(enemy_party, mode=action)


class Hero(Person):
    def __init__(self, name):
        super().__init__(name)
        # overwrite stats here
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

    def choose_action(self, enemy_party):
        #  TODO: find a place to tore possible actions
        possible_actions = ['basic attack', ]
        if len(self.weapons) > 0:
            possible_actions.append('weapon special attack')
        #  basic attack
        #  weapon special attack
        #  spell
        #  inventory
        action = player_choose_from_list(possible_actions)
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

    #  TODO: needs to calculate dmg from super()
    def deal_dmg(self, target):
        dealt_dmg = super().deal_dmg(target)
        self.heal(self.calc_vamp_heal(dealt_dmg))
        return dealt_dmg


class Blocker(Person):
    def __init__(self, name):
        super().__init__(name)
        self.defence = 4
        self.type = 'Blocker'
