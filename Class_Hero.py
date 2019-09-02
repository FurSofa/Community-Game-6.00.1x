from new_npc import *
from helper_functions import *


class Hero(NPC):
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
        print()
        return select_from_list(target_party, index_pos=False, q='Choose a target:')

    def choose_attack(self, attack_options):
        return select_from_list([attack_options[i]['name'] for i in range(len(attack_options))], index_pos=True)

    def choose_battle_action(self, possible_actions):
        """
        lets player choose what to do in their turn and calls appropriate methods
        :param possible_actions:
        :return: -
        """
        #  TODO: find a place to store possible actions
        action = select_from_list(possible_actions, q='What do you want to do?')
        return action


# Testing Code!
if __name__ == '__main__':
    p = NPC.generate('norbnorb', 'Mage')
    p.stat_growth()
    p.show_stats()
    w = Hero.generate('norbnorb', 'Warrior')
    w.calculate_stats()
    print(w.att_dmg_min, end='-')
    print(w.att_dmg_max)
    print(w.calculate_dmg(), end=' ')
    print(w.calculate_dmg(), end=' ')
    print(w.calculate_dmg(), end=' ')
    print(w.calculate_dmg(), end=' ')
    print(w.calculate_dmg(), end=' ')
    print(w.calculate_dmg(), end=' ')
    print(w.calculate_dmg(), end=' ')
    print(w.calculate_dmg(), end=' ')
    print(w.calculate_dmg(), end=' ')
    print(w.calculate_dmg(), end=' ')
    print(w.calculate_dmg(), end=' ')
