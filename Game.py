# Game Class

import person
import Base_Item_Classes
import Combat
import helper_functions
import party




class Game:
    def __init__(self):

        difficulty = input ('Choose difficulty [E]asy, [M]edium, [H]ard: ').lower()
        if difficulty == 'easy' or 'e':
            self.difficulty = 1
        elif difficulty == 'medium' or 'm':
            self.difficulty = 2
        elif difficulty == 'medium' or 'm':
            self.difficulty = 3


    def new_hero(self):
        hero_name = input()
        hero_profession = input()
        our_hero = Hero.generate()

        print(our_hero)
        keep_hero = input('keep this guy? [Y]es or [R]eroll')




