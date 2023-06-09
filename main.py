import player
import pygame as pg
import settings
import sys

from map import Map
from raycasting import RayCasting
from object_renderer import ObjectRenderer
from sprite_object import SpriteObject
from network import Network
from opponent import Opponents


class Game:
    def __init__(self) -> None:
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(settings.RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.player_score = 0
        self.new_game()
        self.opponents = Opponents(self)
        self.mini_map_enabled = False

    def new_game(self):
        self.map = Map(self)
        player_pos = self.map.get_random_free_tile()
        self.player = player.Player(self, player_pos)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.place_donut()
        if settings.NET_ENABLE:
            self.network = Network(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.donut.update()
        self.opponents.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(settings.FPS)
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw(self):
        self.screen.fill('black')
        self.object_renderer.draw()
        self.map.draw()
        self.player.draw()
        self.donut.draw()
        self.opponents.draw()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                if settings.NET_ENABLE:
                    self.network.disconnect()
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN and event.key == pg.K_f:
                pg.display.set_mode(settings.RES, flags=pg.FULLSCREEN)
            if event.type == pg.KEYDOWN and event.key == pg.K_p:
                new_donut_pos = self.map.get_random_free_tile()
                self.place_donut(new_donut_pos)
                if settings.NET_ENABLE:
                    self.network.update_donut(new_donut_pos)

            if event.type == pg.KEYDOWN and event.key == pg.K_r:
                self.player.pos = self.map.get_random_free_tile()

            if event.type == pg.KEYDOWN and event.key == pg.K_m:
                self.mini_map_enabled = not self.mini_map_enabled

    def score(self):
        new_donut_pos = self.map.get_random_free_tile()
        self.place_donut(new_donut_pos)
        if settings.NET_ENABLE:
            self.network.update_donut(new_donut_pos)
        self.player_score += 1

    def place_donut(self, pos=None):
        if not pos:
            pos = self.map.get_random_free_tile()
        self.donut = SpriteObject(self, pos=pos)

    def set_map(self, mini_map):
        self.map.print_map(mini_map)
        self.map = Map(self, mini_map)

    def run(self):
        while True:
            if settings.NET_ENABLE:
                self.network.update()
            self.check_events()
            self.update()
            self.draw()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    # cProfile.run('main', sort='ncalls')
    main()
