import numpy as np
import pygame as pg
from settings import *

class ObjectRenderer:
    def __init__(self, game) -> None:
        self.game = game
        self.screen = game.screen
        self.textures = self.load_textures()
        self.sky_image = self.get_texture('resources/textures/dirt_2.png', (WIDTH, WIDTH))
        self.floor_image = self.get_texture('resources/textures/dirt_2.png', (WIDTH, WIDTH))
        self.sky_offset = 0
        self.floor_offset = 0


    def draw(self):
        pass
        # self.draw_background()
        # self.draw_floor()
        self.render_game_objects()

    def draw_floor(self):
        self.screen.blit(self.floor_image, (0, HALF_HEIGHT, WIDTH, HEIGHT))
        # pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + self.game.player.rel) % WIDTH
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            color = [255 - (255 / (1 + depth ** 5 * 0.00002))] * 3
            image.fill(color, special_flags=pg.BLEND_RGB_SUB)
            self.screen.blit(image, pos)


    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_textures(self):
        return {
            1: self.get_texture('resources/textures/stone_wall.png'),
            2: self.get_texture('resources/textures/wood_2.png'),
            3: self.get_texture('resources/textures/dirt_1.png'),
            4: self.get_texture('resources/textures/dirt_2.png'),
            5: self.get_texture('resources/textures/wood_1.png'),
        }
