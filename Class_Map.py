import copy
import random

from helper_functions import select_from_list
from vfx import clear_screen


class Map:
    def __init__(self, game, base_map, events, p_loc_tx=0, p_loc_ty=0, p_loc_wx=0, p_loc_wy=0):
        self.events = events
        self.known_events = []
        self.base_map = base_map
        self.active_map = ''
        self.game = game
        self.party_loc = {'pos': {
            'w': {'wx': p_loc_wx, 'wy': p_loc_wy,},
            't': {'tx': p_loc_tx, 'ty': p_loc_ty},
        }, 'char': 'O'}

    @property
    def active_tile(self):
        world_row = self.party_loc['pos']['w']['wy']
        world_cell = self.party_loc['pos']['w']['wx']
        return self.base_map[world_row][world_cell]

    @property
    def max_y(self):
        return len(self.active_tile) - 1

    @property
    def max_x(self):
        return len(self.active_tile[0]) - 1

    def draw_map(self, map_data, loc):
        new_map = copy.deepcopy(map_data)
        new_map[loc['pos']['t']['ty']][loc['pos']['t']['tx']] = loc['char']
        return new_map

    def print_map(self, active_map):
        for row in active_map:
            for cell in row:
                print(cell, end=' ')
            print('')

    def print_player_in_map(self):
        active_map = copy.deepcopy(self.active_tile)
        for e in self.events:
            if e['pos']['w'] == self.party_loc['pos']['w']:
                active_map = self.draw_map(active_map, e)
        map_with_player = self.draw_map(active_map, self.party_loc)
        clear_screen()
        self.print_map(map_with_player)
        for e in self.events:
            if self.party_loc['pos'] == e['pos']:
                print(f'an event is triggered!')

    def choose_move(self):
        # build move option list
        loc = self.party_loc
        na_str = ' N/A'
        option_list = ['Left', 'Down', 'Right', 'Camp', 'Up']
        if loc['pos']['t']['ty'] - 1 < 0:
            option_list[4] += na_str
        if loc['pos']['t']['ty'] + 1 > self.max_y:
            option_list[1] += na_str
        if loc['pos']['t']['tx'] - 1 < 0:
            option_list[0] += na_str
        if loc['pos']['t']['tx'] + 1 > self.max_x:
            option_list[2] += na_str
        direction = select_from_list(option_list, q='Move wehre?', horizontal=True)
        if direction[-len(na_str):] == na_str:
            direction = self.choose_move()
        return direction

    def move(self):
        direction = self.choose_move()
        if direction == 'Up':
            self.party_loc['pos']['t']['ty'] -= 1
        elif direction == 'Down':
            self.party_loc['pos']['t']['ty'] += 1
        elif direction == 'Left':
            self.party_loc['pos']['t']['tx'] -= 1
        elif direction == 'Right':
            self.party_loc['pos']['t']['tx'] += 1
        elif direction == 'Camp':
            quit()
            # self.game.camp()

    def run_map(self):
        while True:
            self.print_player_in_map()
            self.move()

    @classmethod
    def generate(cls, game, tile_width=10, tile_rows=10, event_num=10, world_w=2, world_r=2, party_loc_x=0, party_loc_y=0):
        base_map = Map.generate_new_map(world_w, world_r, tile_width, tile_rows)

        events = [
            {'pos': {
                't': {
                    'tx': random.randint(0, tile_width - 1),
                    'ty': random.randint(0, tile_rows - 1)
                },
                'w': {
                    'wx': random.randint(0, world_w - 1),
                    'wy': random.randint(0, world_r - 1),
                }
            }, 'char': num} for num in range(event_num)
        ]

        return cls(game=game, base_map=base_map, events=events, p_loc_tx=party_loc_x, p_loc_ty=party_loc_y)

    @classmethod
    def generate_new_map(cls, world_width=3, world_rows=3, tile_width=3, tile_rows=3):
        base_map = [[[['.' for tc in range(tile_width)] for tr in range(tile_rows)]
                     for wx in range(world_width)] for wy in range(world_rows)]
        return base_map



if __name__ == '__main__':
    m1 = Map.generate(None)
    m1.run_map()
