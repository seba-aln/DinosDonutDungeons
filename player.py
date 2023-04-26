from settings import *
import pygame as pg
import math
import main

class Player:
    def __init__(self, game: main.Game, player_pos) -> None:
        self.game = game
        self.x, self.y = player_pos
        self.angle = PLAYER_ANGLE

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)
        self.check_donut_collision(self.game.donut.pos)

        # if keys[pg.K_LEFT]:
        #     self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        # if keys[pg.K_RIGHT]:
        #     self.angle += PLAYER_ROT_SPEED * self.game.delta_time

        self.angle %= math.tau

    def draw(self):
        pg.draw.line(self.game.screen, 'green', (self.x * MINI_MAP_SCALE, self.y * MINI_MAP_SCALE),
                     (self.x * MINI_MAP_SCALE + 4 * math.cos(self.angle),
                      self.y * MINI_MAP_SCALE + 4 * math.sin(self.angle)), 1)
        pg.draw.circle(self.game.screen, 'green', (self.x * MINI_MAP_SCALE, self.y * MINI_MAP_SCALE), 2)

    def update(self):
        self.movement()
        self.mouse_control()

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def check_wall(self, x, y):
        return(x, y) not in self.game.map.world_map

    def check_donut_collision(self,pos):
        sprite_x, sprite_y = pos
        if int(sprite_x) == int(self.x) and int(sprite_y) == int(self.y):
            self.game.score()


    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE_SCALE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx

        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

    def tile_pos(self):
        return ((self.x % 1), (self.y % 1))
