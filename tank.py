import texturesfile
import base_class
import projectile
import constans


class Tank(base_class.BaseSprite):
    def __init__(self, x: int, y: int, textures=None, owner=constans.COMPUTER_TANK):
        super().__init__(textures, x, y)
        self.height = constans.TANK_HEIGHT
        self.width = constans.TANK_WIDTH
        if owner == constans.COMPUTER_TANK:
            self.textures = {'left': texturesfile.ENEMY_TANK_LEFT, 'right': texturesfile.ENEMY_TANK_RIGHT,
                             'up': texturesfile.ENEMY_TANK_UP, 'down': texturesfile.ENEMY_TANK_DOWN}
        else:
            self.textures = {'left': texturesfile.PLAYER_TANK_LEFT, 'right': texturesfile.PLAYER_TANK_RIGHT,
                             'up': texturesfile.PLAYER_TANK_UP, 'down': texturesfile.PLAYER_TANK_DOWN}

    def shoot(self):
        new_projectile = projectile.Projectile(x=0, y=0)
        new_projectile.current_side = self.current_side
        if self.current_side == 'left':
            new_projectile.y = self.y//2 + constans.BULLET_HEIGHT//2
            new_projectile.x = max(self.x - constans.BULLET_WIDTH, 0)
        elif self.current_side == 'right':
            new_projectile.y = self.y//2 + constans.BULLET_HEIGHT//2
            new_projectile.x = min(self.x + constans.SIDE_OF_BOX, constans.MAP_WIDTH*constans.SIDE_OF_BOX)
        elif self.current_side == 'up':
            new_projectile.y = max(self.y - constans.BULLET_WIDTH, 0)
            new_projectile.x = self.x//2 + constans.BULLET_HEIGHT//2
        else:
            new_projectile.y = min(self.y + constans.SIDE_OF_BOX, constans.MAP_HEIGHT*constans.SIDE_OF_BOX)
            new_projectile.x = self.x//2 + constans.BULLET_HEIGHT//2
        return new_projectile

    def move(self):
        print('moving')
        self.x = self.x + self.move_sides[self.current_side][0]
        self.y = self.y + self.move_sides[self.current_side][1]
        if self.current_side == 'left':
            self.x = max(self.x, 0)
        elif self.current_side == 'right':
            self.x = min(self.x, constans.MAP_WIDTH*constans.SIDE_OF_BOX - self.width)
        elif self.current_side == 'up':
            self.y = max(self.y, 0)
        elif self.current_side == 'down':
            self.y = min(self.y, constans.MAP_HEIGHT*constans.SIDE_OF_BOX - self.height)

    # States - information about neighbour boxes
    def analyse(self, neighbour_states: list):
        pass
