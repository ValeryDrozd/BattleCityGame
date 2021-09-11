import constans
import tank


class Spawn:
    x = 0
    y = 0
    spawn_timer = 0
    height = 0
    width = 0
    last_spawn = -1000

    def __init__(self, x=0, y=0, spawn_timer=0, height=0, width=0):
        self.x = x
        self.y = y
        self.spawn_timer = spawn_timer
        self.width = width
        self.height = height

    def getTank(self):
        return tank.Tank(owner=constans.COMPUTER_TANK, x=self.x, y=self.y)
