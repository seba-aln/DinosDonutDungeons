from sprite_object import *

class Opponents():
    opponents = {}

    def __init__(self, game) -> None:
        self.game = game

    def add(self, uid, opponent):
        self.opponents[uid] = opponent

    def remove(self, uid):
        del(self.opponents[uid])

    def update(self):
        for opponent in self.opponents:
            self.opponents[opponent].update()

    def draw(self):
        for opponent in self.opponents:
            self.opponents[opponent].draw()

    def update_opponent(self, uid, pos):
        if uid not in self.opponents:
            self.opponents[uid] = Opponent(self.game, uid, pos)
        else:
            self.opponents[uid].set_position(pos)


class Opponent():
    previous_position = None
    position = None
    uid = None
    sprite = None

    def __init__(self,game, uid, pos) -> None:
        self.game = game
        self.uid = uid
        self.position = pos
        self.sprite = SpriteObject(self.game, pos=pos, path='resources/sprites/dino.png', color='blue')

    def get_position(self):
        # for now we return last real position. ideally this will calculate vectored positions
        return self.position

    def set_position(self, pos):
        self.previous_position = self.position
        self.position = pos
        self.sprite.x, self.sprite.y = pos

    def update(self):
        self.sprite.update()

    def draw(self):
        self.sprite.draw()
