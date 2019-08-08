# Game Class
from party import Party
import random
from Hero import Hero
from helper_functions import select_from_list


class Game:
    def __init__(self):
        self.party = Party.generate()
        self.autobattle = 0
        self.difficulty = select_from_list(['Easy', 'Medium', 'Hard'], q='Choose your difficulty: ')
        print(f'You selected: {self.difficulty}!')

    def create_character(self, name='Jeb', profession='Astronaut', level=1):
        """
         Create new character
         Allows selection of char and reroll of stats
         """
        return Hero.generate(name, profession, level)

    def create_random_character(self):
        """
         Create new random character the same level as the party leader"""
        level = self.party.member().level
        name = random.choice(['Lamar', 'Stacey', 'Ali', 'Jackson', 'Minky',
                              'Leo', 'Lilli', 'Lindsay', 'Tongo', 'Paku', ])
        profession = random.choice(['Warrior', 'Archer', 'Mage', 'Farmer', 'Blacksmith'])
        return Hero.generate(name, profession, level)

    def create_hero(self):

        def reroll_stats(hero_name, hero_profession):
            our_hero = self.create_character(hero_name, hero_profession)
            our_hero.show_stats()
            return our_hero

        hero_name = input('What is your name, hero?:\n').title()
        if len(hero_name) > 0:
            print(f'{hero_name}, ah yes. That name carries great respect!')

        else:
            print('Ah, the quiet type huh? I\'ll just call you Steve.')
            hero_name = 'Steve'

        hero_profession = select_from_list(['Warrior', 'Archer', 'Mage'],
                                           q=f'Now, {hero_name}, What is your profession?:\n')
        print(f'You look like a great {hero_profession}, {hero_name}. I should have guessed.')
        while True:
            our_hero = reroll_stats(hero_name, hero_profession)
            keep_hero = input('Do you want to keep these stats? \n[Y]es or [R]eroll Hero\n').lower()
            if keep_hero == '':
                return our_hero
            elif keep_hero == 'y':
                return our_hero
            else:
                continue

    def adventure(self):
        print(f'You found another traveler You talk for a while and have a great time!')
        self.party.add_member(self.create_random_character())
        print('Time to get back to the task at hand!')

    def camp(self):
        print('A bear got into the camp and killed everyone!')
        self.party.kill_everyone()

    def main_options(self):
        """
        Contains Choices after new game and settings
        """

        def adventure(self):
            print(f'You found another traveler You talk for a while and have a great time!')
            self.party.add_member(self.create_random_character())
            print('Time to get back to the task at hand!')

        def camp(self):
            print('A bear got into the camp and killed everyone!')
            self.party.kill_everyone()

        choice = select_from_list(['Adventure', 'Camp', 'Party Info'], True, q=f'What would you like to do\n ')
        if choice == 0:
            self.adventure()
        elif choice == 1:
            self.camp()
        elif choice == 2:
            self.party.party_members_info()

    def game_over(self):
        print('Game Over, Thanks for playing!')

        quit()

    def gameloop(self):
        self.party.add_member(self.create_hero())
        print(f'You are all set! Danger is that way, Good Luck, {self.party.member().name}!\n')
        while self.party.has_units_left:
            self.main_options()

        self.game_over()


# new_game = Game()
# new_game.gameloop()
