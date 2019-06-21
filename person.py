import random


class Person:
    def __init__(self, name):
        self.name = name
        self.type = 'Base NPC'
        self.max_health = 20
        self.health = self.max_health
        self.attack_dmg = 5
        self.defence = 1
        self.inventory = []
        self.gold = 0
        self.crit_chance = 5
        self.crit_dmg = 150
        self.party = None

    def __repr__(self):
        return self.name + ', ' + self.type

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def take_dmg(self, dmg_amount):
        dmg_taken = dmg_amount - self.defence
        if dmg_taken < 0:
            dmg_taken = 0
        self.health -= dmg_taken
        return dmg_taken

    def calculate_dmg(self):
        dmg = self.attack_dmg
        if random.randrange(100) < self.crit_chance:
            dmg = dmg * self.crit_dmg // 100
            print(self, 'lands a critical strik!')
        return dmg

    def deal_dmg(self, target):
        dealt_dmg = self.calculate_dmg()
        dmg_dealt = target.take_dmg(dealt_dmg)
        return dmg_dealt

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
            print(self, 'is fully Healed!')
        else:
            print(self, 'healed for', amount, 'hp')
        return amount

    def change_gold(self, gold_amount):
        #  check if person has enough gold might be better in merchant class
        if self.gold + gold_amount < 0:
            print('Not enough gold!')
            return 'Error'
        self.gold += gold_amount
        return gold_amount

    def choose_target(self, target_party):
        if len(target_party.members) > 1:
            choice = random.randrange(len(target_party.members)-1)
        else:
            choice = 0
        return target_party.members[choice]

    def attack_target(self, target_party):
        target = self.choose_target(target_party)
        print('target:', target)
        dmg_enemy_received = self.deal_dmg(target)
        print(self, 'deals', dmg_enemy_received, 'to', target)
        print('target hp:', target.health)


class Hero(Person):
    def __init__(self, name):
        super().__init__(name)
        # overwrite stats here
        self.max_health = 40
        self.health = self.max_health
        self.type = 'Hero'
        self.crit_chance = 10
        self.attack_dmg = 6
        self.defence += 1

    def choose_target(self, target_party):
        print('Choose a target:')
        for i, member in enumerate(target_party.members):
            print(i+1, member)
        choice = input('Target number: ')
        if not choice.isdigit() or not 0 < int(choice) < len(target_party.members) + 1:
            print('Enter the number of the target!')
            self.choose_target(target_party.members)
        return target_party.members[int(choice)-1]


#  example on how to modify methods
class Vampire(Person):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'Vampire'
        self.vampirism = 50
        self.defence = 0

    def calc_vamp_heal(self, dealt_dmg):
        return dealt_dmg // (100 // self.vampirism)

    def deal_dmg(self, target):
        dealt_dmg = super().deal_dmg(target)
        self.heal(self.calc_vamp_heal(dealt_dmg))
        return dealt_dmg


class Blocker(Person):
    def __init__(self, name):
        super().__init__(name)
        self.defence = 4
        self.type = 'Blocker'
