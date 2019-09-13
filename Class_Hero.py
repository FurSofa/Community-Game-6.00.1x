from Class_NPC import *
from helper_functions import *
from data_src import *


class Hero(NPC):
    def __init__(self, name, profession, u_type, worth_xp,
                 base_stats,
                 spell_book, equip_slots, tracked_values,
                 hero=True, level=1, xp=0, next_level=20):
        super().__init__(name, profession, u_type, worth_xp,
                         base_stats,
                         spell_book, equip_slots, tracked_values,
                         hero, level, xp, next_level)
        # _ = unit_type
        # self.type = 'Hero'

    @classmethod
    def generate(cls, name='Mr. Lazy', profession='Warrior', level=1, type='Hero'):
        return cls(name, profession, level, new_char, type=type)


    @classmethod
    def generate_random(cls, level=1, type='Hero'):
        """
        Create new random character at level 1
        """
        level = level
        # name = random.choice(['Lamar', 'Colin', 'Ali', 'Jackson', 'Minky',
        #                       'Leo', 'Phylis', 'Lindsay', 'Tongo', 'Paku', ])
        # profession = random.choice(['Warrior', 'Archer', 'Mage', 'Blacksmith', 'Thief', 'Bard'])
        _ = type
        profession = random.choice([p for p in data.hero_classes.keys()])
        name = random.choice(data.hero_classes[profession]['names'])

        # if name == 'Minky':
        #     profession = 'Miffy Muffin'
        # if name == 'Colin':
        #     profession = 'Bard of Bass'
        return cls(name, profession, level, type='Hero')


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

    def get_data(self):
        return get_data_from_keys(data, ['heroes'])

    # def get_class_data(self):
    #     class_key = self.profession
    #     return self.get_data()[class_key]

# Testing Code!
if __name__ == '__main__':
    p = NPC.generate('norbnorb', 'Mage')
    p.stat_growth()
    p.show_stats()
    w = Hero.generate('norbnorb', 'Warrior')
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
