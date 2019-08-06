# Game Class


import Hero
from helper_functions import player_choose_from_list


class Game:
    def __init__(self):

        difficulty = input('Choose difficulty [E]asy, [M]edium, [H]ard: \n').lower()
        if difficulty == 'easy' or 'e':
            self.difficulty = 1
        elif difficulty == 'medium' or 'm':
            self.difficulty = 2
        elif difficulty == 'hard' or 'h':
            self.difficulty = 3
        else:
            self.difficulty = 1

    def new_hero(self):
        hero_name = input('whats your name?: ')
        hero_profession = input(f'what is your profession?:\n[W]arrior, [A]rcher, [M]age\n').lower()
        if hero_profession == 'w':
            hero_profession = 'warrior'
        elif hero_profession == 'a':
            hero_profession = 'archer'
        elif hero_profession == 'm':
            hero_profession = 'mage'
        else:
            hero_profession = 'warrior'

        our_hero = Hero.Hero.generate(hero_name, hero_profession)
        hero_name = input()
        hero_profession = player_choose_from_list(['Warrior', 'Archer', 'Mage'])
        our_hero = Hero.generate()

        print(our_hero)
        keep_hero = input('Do you want to keep this Hero? \n[Y]es or [R]eroll\n').lower()
        if keep_hero == 'r':
            self.new_hero()
        else:
            pass
        return our_hero

    def gameloop(self):
        while True:
            our_hero = self.new_hero()
            print('game started')
            print(our_hero)
            print('Ask about adventuring..')
            print('You died of old age, great work!')
            break
        print('game over.')


new_game = Game()
new_game.gameloop()



