import person
from helper_functions import select_from_list


class Hero(person.Person):
    def __init__(self, name, profession, level):
        super().__init__(name, profession, level)
        self.type = 'Hero'

    @classmethod
    def generate(cls, name='Mr. Lazy', profession='warrior', level=1):
        return cls(name, profession, level)

    def __str__(self):
        return super().__str__()

    def choose_target(self, target_party):
        """
        chooses a person to attack
        :param target_party: party instance
        :return: person instance
        """
        print('Choose a target:')
        return select_from_list(target_party.members)

    def choose_battle_action(self, enemy_party):
        """
        ENDPOINT for battle
        lets player choose what to do in their turn and calls appropriate methods
        :param enemy_party: party instance
        :return: -
        """
        #  TODO: find a place to store possible actions
        possible_actions = ['basic attack', ]
        if self.main_hand:
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
        action = select_from_list(possible_actions)
        if action == 'change gear':
            self.change_gear()
            self.choose_battle_action(enemy_party)
        elif action == 'Show Hero Stats':
            print(self.show_stats())
            self.choose_battle_action(enemy_party)
        self.attack_target(enemy_party, mode=action)

# Testing Code!
# p = person.Person.generate('norbnorb', 'Mage')
# p.profession_stat_augment()
# print(p)
#
# w = Hero.generate('norbnorb', 'Warrior')
# w.profession_stat_augment()
# print(w)
