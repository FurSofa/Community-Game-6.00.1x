import random


class Person:
    def __init__(self, name):
        self.name = name
        self.max_health = 20
        self.health = self.max_health
        self.attack_dmg = 5
        self.defence = 2
        self.inventory = []
        self.gold = 0

    def __repr__(self):
        return self.name

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def take_dmg(self, dmg_amount):
        dmg_taken = dmg_amount - self.defence
        if dmg_taken < 0:
            dmg_taken = 0
        self.health -= dmg_taken
        return dmg_taken

    def deal_dmg(self, target):
        dealt_dmg = self.attack_dmg
        dmg_dealt = target.take_dmg(dealt_dmg)
        return dmg_dealt

    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
        return amount

    def change_gold(self, gold_amount):
        self.gold += gold_amount
        return gold_amount

    def choose_target(self, target_party):
        choice = random.randrange(len(target_party)-1)
        print(target_party[choice])
        return target_party[choice]

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

    def choose_target(self, target_party):
        print('Choose a target:')
        for i, member in enumerate(target_party):
            print(i+1, member)
        choice = input('Target number: ')
        if not choice.isdigit() or not 0 < int(choice) < len(target_party) + 1:
            print('Enter the number of the target!')
            self.choose_target(target_party)
        return target_party[int(choice)-1]


