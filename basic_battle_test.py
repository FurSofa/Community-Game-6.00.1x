from new_npc import *
from Class_Hero import Hero

class DGame:
    def __init__(self, difficulty):
        self.difficulty = difficulty
dummy_game = DGame('Easy')

from Class_Party import Party
from battle import *
npc1=Hero('h1', 'thief', 1)
npc2=NPC()
p1 = Party(dummy_game)
p2 = Party(dummy_game)
p1.add_member(npc1)
p2.add_member(npc2)
