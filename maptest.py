from types import SimpleNamespace
from time import sleep
import random
import copy

from helper_functions import select_from_list
from vfx import clear_screen


# old_map = [
#     ['.', '.', '.'],
#     ['.', '.', '.'],
#     ['.', '.', '.'],
# ]

player_loc = SimpleNamespace(x=0, y=0, char='o')
event_loc = SimpleNamespace(x=0, y=2, char='x')


def choose_move(loc):
    direction = select_from_list(['Left', 'Down', 'Right', 'quit', 'Up'], q='Move wehre?', horizontal=True)
    if direction == 'Up':
        loc.y -= 1
    elif direction == 'Down':
        loc.y += 1
    elif direction == 'Left':
        loc.x -= 1
    elif direction == 'Right':
        loc.x += 1
    elif direction == 'quit':
        quit()
    return loc


def draw_map(old_map, loc):
    new_map = old_map.copy()
    new_map[loc.y][loc.x] = loc.char
    return new_map


def printmap(map):
    for row in map:
        for cell in row:
            print(cell, end=' ')
        print('')


def print_player_in_map(p_loc, base_map, events):
    # base_map = [['.' for c in range(cells)] for row in range(rows)]
    active_map = base_map.copy()
    for e in events:
        active_map = draw_map(active_map, e)
    map_with_player = draw_map(active_map, p_loc)
    clear_screen()
    printmap(map_with_player)
    for e in events:
        if p_loc.x == e.x and p_loc.y == e.y:
            print(f'an event is triggered!')


def run_map(player_loc, base_map, events):
    while True:

        print_player_in_map(player_loc, copy.deepcopy(base_map), events)
        player_loc = choose_move(player_loc)


if __name__ == '__main__':
    rows = 10
    cells = 10
    event_num = 5

    base_map = [['.' for c in range(cells)] for row in range(rows)]

    events = [SimpleNamespace(x=random.randint(0, cells-1), y=random.randint(0, rows-1), char='x') for i in range(event_num)]
    run_map(player_loc, base_map, events)

    # print_player_in_map(p_loc)
    # sleep(1)
    # p_loc.x += 1
    # print_player_in_map(p_loc)
    # sleep(1)
    # p_loc.x += 1
    # print_player_in_map(p_loc)
    # sleep(1)
    # p_loc.y += 1
    # print_player_in_map(p_loc)
    # sleep(1)
    # p_loc.y += 1
    # print_player_in_map(p_loc)
    # sleep(1)
    # p_loc.x += -1
    # print_player_in_map(p_loc)
    # sleep(1)
    # p_loc.x += -1
    # print_player_in_map(p_loc)
