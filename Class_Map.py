import copy
import random

from helper_functions import select_from_list
from vfx import clear_screen


class Map:
    def __init__(self, game, base_map, events, party_loc_x=0, party_loc_y=0):
        self.events = events
        self.known_events = []
        self.base_map = base_map
        self.active_map = ''
        self.game = game
        self.max_y = len(base_map)-1
        self.max_x = len(base_map[0])-1
        self.party_loc = {'pos': {'x': party_loc_x, 'y': party_loc_y}, 'char': 'O'}

    def draw_map(self, map_data, loc):
        new_map = copy.deepcopy(map_data)
        new_map[loc['pos']['y']][loc['pos']['x']] = loc['char']
        return new_map

    def print_map(self, active_map):
        for row in active_map:
            for cell in row:
                print(cell, end=' ')
            print('')

    def print_player_in_map(self):
        active_map = copy.deepcopy(self.base_map)
        for e in self.events:
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
        if loc['pos']['y'] - 1 < 0:
            option_list[4] += na_str
        if loc['pos']['y'] + 1 > self.max_y:
            option_list[1] += na_str
        if loc['pos']['x'] - 1 < 0:
            option_list[0] += na_str
        if loc['pos']['x'] + 1 > self.max_x:
            option_list[2] += na_str
        direction = select_from_list(option_list, q='Move wehre?', horizontal=True)
        if direction[-len(na_str):] == na_str:
            direction = self.choose_move()
        return direction

    def move(self):
        direction = self.choose_move()
        if direction == 'Up':
            self.party_loc['pos']['y'] -= 1
        elif direction == 'Down':
            self.party_loc['pos']['y'] += 1
        elif direction == 'Left':
            self.party_loc['pos']['x'] -= 1
        elif direction == 'Right':
            self.party_loc['pos']['x'] += 1
        elif direction == 'Camp':
            quit()
            # self.game.camp()

    def run_map(self):
        while True:
            self.print_player_in_map()
            self.move()

    @classmethod
    def generate(cls, game, width=10, rows=10, event_num=10, party_loc_x=0, party_loc_y=0):
        base_map = [['.' for cell in range(width)] for row in range(rows)]

        events = [{'pos': {'x': random.randint(0, width - 1), 'y': random.randint(0, rows - 1)},
                   'char': 'x'} for _ in range(event_num)]

        return cls(game=game, base_map=base_map, events=events, party_loc_x=party_loc_x, party_loc_y=party_loc_y)


if __name__ == '__main__':
    m1 = Map.generate(None)
    m1.run_map()
