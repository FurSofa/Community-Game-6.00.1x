from types import SimpleNamespace

from Class_NPC import *
from Class_Hero import Hero
from battle import *
from Class_Party import Party

dummy_game = SimpleNamespace(difficulty='Easy')


npc1 = Hero('h1', 'thief', 1)
npc2 = NPC()
p1 = Party(dummy_game)
p2 = Party(dummy_game)
p1.add_member(npc1)
p2.add_member(npc2)
