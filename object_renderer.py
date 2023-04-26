import pygame as pg
import settings


class ObjectRenderer:
    def __init__(self, game) -> None:
        self.game = game
        self.screen = game.screen
        self.textures = self.load_textures()
        self.sky_image = self.get_texture('resources/textures/dirt_2.png', (settings.WIDTH, settings.WIDTH))
        self.floor_image = self.get_texture('resources/textures/dirt_2.png', (settings.WIDTH, settings.WIDTH))
        self.sky_offset = 0
        self.floor_offset = 0

    def draw(self):
        pg.draw.rect(self.screen, settings.FLOOR_COLOR, (0, settings.HALF_HEIGHT, settings.WIDTH, settings.HEIGHT))
        self.render_game_objects()

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            color = [255 - (255 / (1 + depth ** 5 * 0.00002))] * 3
            image.fill(color, special_flags=pg.BLEND_RGB_SUB)
            self.screen.blit(image, pos)

    @staticmethod
    def get_texture(path, res=(settings.TEXTURE_SIZE, settings.TEXTURE_SIZE)):
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
