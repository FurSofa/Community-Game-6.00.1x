from helper_functions import select_from_list
from person import NPC, Hero
from party import Party
from battle import Battle
from weapons import Sword

# TODO: Move this to Game.py and add if name == __Main__:

player_name = input('What is your name, Traveler?')

hero_party = Party()

hero = Hero(player_name)  # todo: make stats args (name, class_type, ??)

hero_party.add_member(hero)

while hero_party.has_units_left:
    print('What would you like to do, ' + str(hero.name) + '?')
    player_action = select_from_list(['BATTLE!', 'camp'])
    if player_action == 'BATTLE!':

        # todo: make it a method
        enemy_party = Party()
        enemy1 = NPC('Goomba')
        enemy_party.add_member(enemy1)
        battle = Battle()
        hero_won = battle.alternating_turn_battle(hero_party, enemy_party)
        if hero_won:
            # todo: generate loot
            print('You got loot!')
            loot = Sword(15, 3)
            hero.pickup_gear(loot)
    elif player_action == 'camp':
        # todo: make a camp
        print('we need some kind of camp here guys')
