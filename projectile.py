import base_class
import constans
import texturesfile


class Projectile(base_class.BaseSprite):
    def __init__(self, x: int, y: int, textures=None):
        super().__init__(textures, x, y)
        self.height = constans.BULLET_HEIGHT
        self.width = constans.BULLET_WIDTH
        self.in_move = True
        self.speed = 5
        self.owner = 0
        if textures is None:
            self.textures = {'left': texturesfile.BULLET_LEFT, 'right': texturesfile.BULLET_RIGHT,
                             'up': texturesfile.BULLET_UP, 'down': texturesfile.BULLET_DOWN}
