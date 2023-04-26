from random import randint
import pygame as pg

from settings import MINI_MAP_SCALE, MAP_SIZE_X, MAP_SIZE_Y, MAP_COMPLEXITY

_ = False
mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 2, 2, 2, 2, _, _, 5, 5, _, _, _, 1],
    [1, _, _, _, _, 2, _, _, _, _, 5, _, _, _, 1],
    [1, _, _, _, 2, _, _, _, _, _, 5, 5, 5, 5, 1],
    [1, _, _, _, 2, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, 4, _, _, _, 1],
    [1, 3, 3, 3, 3, 3, _, 4, 4, 4, 4, _, _, _, 1],
    [1, _, _, _, _, _, _, _, 4, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]


class Map:
    def __init__(self, game, mini_map=None) -> None:
        self.border_id = 1
        self.wall_id = 2
        self.game = game
        if mini_map:
            self.mini_map = mini_map
        else:
            self.mini_map = self.generate_map(MAP_SIZE_X, MAP_SIZE_Y, MAP_COMPLEXITY)
        self.world_map = {}
        self.get_map()

    def generate_map(self, map_size_x, map_size_y, walls=2):
        walls = min(walls, (min(map_size_x, map_size_y) // 7))
        mini_map = [[1] + [_] * (map_size_x - 2) + [1] for x in range(map_size_y)]
        mini_map[0] = mini_map[map_size_y - 1] = [1] * map_size_x
        if walls == 0:
            return mini_map
        x_segment = map_size_x // walls
        y_segment = map_size_y // walls

        walls_x = []
        walls_y = []
        for wall in range(walls):
            wall_x = randint(3, x_segment - 3) + wall * x_segment
            walls_x.append(wall_x if wall_x < map_size_x - 3 else map_size_x - 4)

            wall_y = randint(3, y_segment - 3) + wall * y_segment
            walls_y.append(wall_y if wall_y < map_size_y - 3 else map_size_y - 4)

        for row in walls_y:
            mini_map[row] = [val if val else self.wall_id for col, val in enumerate(mini_map[row])]
            # punching holes
            last_seg = 0
            for seg in walls_y:
                mini_map[row][randint(last_seg + 1, seg - 1)] = _
                mini_map[row][randint(last_seg + 1, seg - 1)] = _
                mini_map[row][randint(last_seg + 1, seg - 1)] = _
                last_seg = seg
            mini_map[row][randint(last_seg + 1, map_size_y - 2)] = _
            mini_map[row][randint(last_seg + 1, map_size_y - 2)] = _
            mini_map[row][randint(last_seg + 1, map_size_y - 2)] = _

        for col in walls_x:
            for row, map_row in enumerate(mini_map):
                if not mini_map[row][col]:
                    mini_map[row][col] = self.wall_id
            last_seg = 0
            for seg in walls_x:
                mini_map[randint(last_seg + 1, seg - 1)][col] = _
                mini_map[randint(last_seg + 1, seg - 1)][col] = _
                mini_map[randint(last_seg + 1, seg - 1)][col] = _
                last_seg = seg
            mini_map[randint(last_seg + 1, map_size_y - 2)][col] = _
            mini_map[randint(last_seg + 1, map_size_y - 2)][col] = _
            mini_map[randint(last_seg + 1, map_size_y - 2)][col] = _

        self.print_map(mini_map)

        return mini_map

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[i, j] = value

    def print_map(self, mini_map=False):
        if not mini_map:
            mini_map = self.mini_map

        for row in mini_map:
            print(''.join(['x' if c else ' ' for c in row]))

    def get_random_free_tile(self, offset_x=0.5, offset_y=0.5):
        while True:
            col = randint(1, len(self.mini_map[0]) - 2)
            row = randint(1, len(self.mini_map) - 2)
            if not self.mini_map[row][col]:
                break
        return col + offset_x, row + offset_y

    def draw(self):
        if self.game.mini_map_enabled:
            for pos in self.world_map:
                pg.draw.rect(
                    self.game.screen, 'gray',
                    (pos[0] * MINI_MAP_SCALE, pos[1] * MINI_MAP_SCALE, MINI_MAP_SCALE, MINI_MAP_SCALE),
                    2)
