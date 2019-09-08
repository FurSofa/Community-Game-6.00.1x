import copy
import random

from helper_functions import select_from_list
from vfx import clear_screen


rand_event_chance = 30

class Map:
    def __init__(self, game, base_map, events, p_loc_tx=0, p_loc_ty=0, p_loc_wx=0, p_loc_wy=0):
        self.events = events
        self.known_events = []
        self.base_map = base_map
        self.game = game
        self.party_loc = {'pos': {
            'w': {'x': p_loc_wx, 'y': p_loc_wy,},
            't': {'x': p_loc_tx, 'y': p_loc_ty},
        }, 'char': 'o'}

    @property
    def active_base_tile(self):
        world_row = self.party_loc['pos']['w']['y']
        world_cell = self.party_loc['pos']['w']['x']
        return self.base_map[world_row][world_cell]

    @property
    def active_tile(self):
        return self.get_map_tile(self.party_loc['pos'])

    def get_base_map_tile(self, pos):
        w_loc = pos['w']
        world_row = w_loc['y']
        world_cell = w_loc['x']
        return self.base_map[world_row][world_cell]

    def get_map_tile(self, pos):
        map_tile = copy.deepcopy(self.get_base_map_tile(pos))
        for e in self.events:
            if e['pos']['w'] == pos['w']:
                map_tile = self.draw_map(map_tile, e)
        return map_tile

    @property
    def max_y(self):
        return len(self.active_tile) - 1

    @property
    def max_x(self):
        return len(self.active_tile[0]) - 1

    def draw_map(self, map_data, loc):
        new_map = copy.deepcopy(map_data)
        new_map[loc['pos']['t']['y']][loc['pos']['t']['x']] = loc['char']
        return new_map

    def print_map(self, active_map):
        coordinat_str = f'X: {self.party_loc["pos"]["w"]["x"]} / Y: {self.party_loc["pos"]["w"]["y"]}'
        print(f'{coordinat_str:^18}')
        for row in active_map:
            for cell in row:
                print(cell, end=' ')
            print('')

    def print_player_in_map(self):
        active_map = copy.deepcopy(self.active_tile)
        map_with_player = self.draw_map(active_map, self.party_loc)
        clear_screen()
        self.print_map(map_with_player)

    def event_check(self):
        for e in self.events:
            if self.party_loc['pos'] == e['pos']:
                print(f'an event is triggered!')
                return e
        return None

    def move(self):
        direction = self.choose_move()
        if direction == 'Camp':
            return direction
        move = self.build_move(direction)
        if self.eval_move(move):
            self.make_move(move)
        else:
            move = self.build_move(direction, scope='w')
            if self.eval_move(move):
                self.make_move(move)
            else:
                print('Move impossible')
                self.move()

    def make_move(self, move):
        self.party_loc = self.sum_pos(self.party_loc, move)

    def choose_move(self):
        option_list = ['Left', 'Down', 'Right', 'Camp', 'Up']
        direction = select_from_list(option_list, q='Move where?', horizontal=True)
        return direction

    def build_move(self, direction, scope='t', ):
        move = {'pos': {'w': {'x': 0, 'y': 0}, 't': {'x': 0, 'y': 0}}, 'char': ''}
        if direction == 'Up':
            move['pos'][scope]['y'] -= 1
            if scope == 'w':
                move['pos']['t']['y'] = self.max_y
        elif direction == 'Down':
            move['pos'][scope]['y'] += 1
            if scope == 'w':
                move['pos']['t']['y'] = -self.max_y
        elif direction == 'Left':
            move['pos'][scope]['x'] -= 1
            if scope == 'w':
                move['pos']['t']['x'] = self.max_x
        elif direction == 'Right':
            move['pos'][scope]['x'] += 1
            if scope == 'w':
                move['pos']['t']['x'] = -self.max_x
        return move

    def sum_pos(self, pos1, pos2):
        new_pos = {'pos': {}}
        for scope in pos1['pos'].keys():
            new_pos['pos'][scope] = {}
            for loc in pos1['pos'].get(scope).keys():
                new_pos['pos'][scope][loc] = pos1['pos'][scope].get(loc) + pos2['pos'][scope].get(loc)
        new_pos['char'] = pos1['char']
        return new_pos

    def eval_move(self, move):
        new_loc = self.sum_pos(self.party_loc, move)
        w_pos = [n for n in new_loc['pos']['w'].values()]
        t_pow = [t for t in new_loc['pos']['t'].values()]
        if any([v < 0 for v in w_pos + t_pow]):
            return False
        try:
            self.draw_map(self.get_map_tile(new_loc['pos']), new_loc)
            print('move success')
            return True
        except IndexError:
            return False

    def run_map(self):
        while True:
            self.print_player_in_map()
            self.move()
            event = self.event_check()
            if event:
                print(f'{event.get("description")}')
                return event
            else:
                if random.randint(0, 100) < rand_event_chance:
                    return 'random'


    @classmethod
    def generate(cls, game, tile_width=8, tile_rows=8, event_num=30, world_w=2, world_r=2, party_loc_x=0, party_loc_y=0):
        base_map = Map.generate_new_map(world_w, world_r, tile_width, tile_rows)

        events = [
            {
                'pos': {
                    't': {
                        'x': random.randint(0, tile_width - 1),
                        'y': random.randint(0, tile_rows - 1)
                    },
                    'w': {
                        'x': random.randint(0, world_w - 1),
                        'y': random.randint(0, world_r - 1),
                    }
                },
                'char': 'x',
                'description': f'Event Nr {num + 1}'
            } for num in range(event_num)
        ]

        return cls(game=game, base_map=base_map, events=events, p_loc_tx=party_loc_x, p_loc_ty=party_loc_y)

    @classmethod
    def generate_new_map(cls, world_width=3, world_rows=3, tile_width=3, tile_rows=3):
        base_map = [[[['.' for tc in range(tile_width)] for tr in range(tile_rows)]
                     for wx in range(world_width)] for wy in range(world_rows)]
        return base_map

    def serialize(self):
        dummy = self.__dict__.copy()
        dummy['game'] = None
        return dummy

    @classmethod
    def deserialize(cls, save_data):
        dummy = cls.generate(None)
        dummy.__dict__ = save_data.copy()
        return dummy


a = {'pos': {'w': {'x': 1, 'y': 1}, 't': {'x': 0, 'y': 0}}, 'char': '#'}

if __name__ == '__main__':
    m1 = Map.generate(None)
    m1.run_map()
