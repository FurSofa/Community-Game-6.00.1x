from types import SimpleNamespace

from Class_NPC import *
from Class_Hero import Hero
from battle import *
from Class_Party import Party

dummy_game = SimpleNamespace(difficulty='Easy')


npc1 = Hero.generate_unit('heroes/bases/rng', 1, 'testor')
npc2 = NPC.generate_unit('enemies/trash/rng', 1)
p1 = Party(dummy_game)
p2 = Party(dummy_game)
p1.add_member(npc1)
p2.add_member(npc2)
