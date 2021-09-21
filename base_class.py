import constans


class BaseSprite:
    textures = {'left': '', 'right': '', 'up': '', 'down': ''}
    sides = ['left', 'right', 'up', 'down']
    x: int = 0
    y: int = 0
    height: int = 0
    width: int = 0
    in_move: bool = False
    current_side: str = 'left'
    speed: int = 3
    move_sides: dict = {'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}
    reload_time = 1000
    last_shot = -5000
    owner = 0

    def __init__(self, textures: dict, x: int, y: int, in_move: bool = False, current_side='left'):
        self.textures = textures
        self.current_side = current_side
        self.x = x
        self.y = y
        self.last_x = -1
        self.last_y = -1
        self.in_move = in_move
        self.current_side = current_side


    def move(self):
        self.x = self.x + self.move_sides[self.current_side][0]*self.speed
        self.y = self.y + self.move_sides[self.current_side][1]*self.speed
        if self.current_side == 'left':
            self.x = max(self.x, 0)
        elif self.current_side == 'right':
            self.x = min(self.x, constans.MAP_WIDTH*constans.SIDE_OF_BOX - self.width)
        elif self.current_side == 'up':
            self.y = max(self.y, 0)
        elif self.current_side == 'down':
            self.y = min(self.y, constans.MAP_HEIGHT*constans.SIDE_OF_BOX - self.height)
