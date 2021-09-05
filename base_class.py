class BaseSprite:
    textures = {'left': '', 'right': '', 'up': '', 'down': ''}
    sides = ['left', 'right', 'up', 'down']
    x: int = 0
    y: int = 0
    height: int = 0
    width: int = 0
    in_move: bool = False
    current_side: str = 'left'
    self_move_speed: int = 100
    move_sides: dict = {'left': (-1, 0), 'right': (1, 0), 'up': (0, -1), 'down': (0, 1)}

    def __init__(self, textures: dict, x: int, y: int, in_move: bool = False, current_side='left'):
        self.textures = textures
        self.current_side = current_side
        self.x = x
        self.y = y
        self.in_move = in_move
        self.current_side = current_side

    def move(self):
        if self.in_move:
            self.x = self.x + self.move_sides[self.current_side][0]
            self.y = self.x + self.move_sides[self.current_side][1]
