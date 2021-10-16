import math
from minimax import FieldState, minimax
from bfs import bfs
from check_move_possibility import change_nodes
from a_star import a_star
import random

import texturesfile
import base_class
import projectile
import constans
from tree_building import tree_build


class Tank(base_class.BaseSprite):
    def __init__(self, x: int, y: int, textures=None, owner=constans.COMPUTER_TANK):
        super().__init__(textures, x, y)
        self.height = constans.TANK_HEIGHT
        self.width = constans.TANK_WIDTH
        self.speed = 1
        self.owner = owner
        # self.target = (10*constans.SIDE_OF_BOX, 10*constans.SIDE_OF_BOX)
        self.path = []
        self.timer_sleep = 20
        self.reload_time = 2000
        if owner == constans.COMPUTER_TANK:
            self.textures = {'left': texturesfile.ENEMY_TANK_LEFT, 'right': texturesfile.ENEMY_TANK_RIGHT,
                             'up': texturesfile.ENEMY_TANK_UP, 'down': texturesfile.ENEMY_TANK_DOWN}
            self.hp = 1
        else:
            # self.reload_time = 200
            self.textures = {'left': texturesfile.PLAYER_TANK_LEFT, 'right': texturesfile.PLAYER_TANK_RIGHT,
                             'up': texturesfile.PLAYER_TANK_UP, 'down': texturesfile.PLAYER_TANK_DOWN}
            self.hp = 3

    def shoot(self):
        new_projectile = projectile.Projectile(x=0, y=0)
        new_projectile.current_side = self.current_side
        new_projectile.owner = self.owner
        if self.current_side == 'left':
            new_projectile.y = self.y + self.height // 2 - constans.BULLET_HEIGHT // 2
            new_projectile.x = max(self.x - constans.BULLET_WIDTH, 0)
        elif self.current_side == 'right':
            new_projectile.y = self.y + self.height // 2 - constans.BULLET_HEIGHT // 2
            new_projectile.x = min(self.x + self.width,
                                   constans.MAP_WIDTH * constans.SIDE_OF_BOX)
        elif self.current_side == 'up':
            new_projectile.y = max(self.y - constans.BULLET_WIDTH, 0)
            new_projectile.x = self.x + self.width // 2 - constans.BULLET_HEIGHT // 2
        else:
            new_projectile.y = min(
                self.y + constans.TANK_HEIGHT, constans.MAP_HEIGHT * constans.SIDE_OF_BOX)
            new_projectile.x = self.x + self.width // 2 - constans.BULLET_HEIGHT // 2
        return new_projectile

    # States - information about neighbour boxes
    def analyse(self, state):
        if state:
            self.current_side = random.choice(self.sides)

    def move_minimax(self, game_map, target):
        self.timer_sleep -= 1

        if self.x % constans.SIDE_OF_BOX == 0 and self.y % constans.SIDE_OF_BOX == 0 and self.timer_sleep <= 0:
            state = FieldState(game_map)
            
            target_position = change_nodes(target)
            player_position = change_nodes((self.x, self.y))

            root_node = tree_build(state, target_position)
            best_value = minimax(root_node, -math.inf, math.inf, 0)
            # best_value = expectimax(self.root_node, 0)

            for child in root_node.children:
                if child.value == best_value:
                    new_position = child.state.get_player_position()
                    # print("player_position: " + str(player_position))
                    
                    # print("new_position" + str(new_position))
                    delta = (-player_position[0] + new_position[0],
                            -player_position[1] + new_position[1])
                    # print("delta" + str(delta))
                    delta_arr = self.move_sides.items()
                    new_side = 'left'
                    for item in delta_arr:
                        if item[1] == delta:
                            new_side = item[0]
                            break
                    # print(new_side)
                    self.current_side = new_side
                    self.last_x = self.x
                    self.last_y = self.y
                    if new_position == target_position:
                        return 1
                    break

        # self.move()

    def auto_move(self, game_map, target):
        self.timer_sleep -= 1

        if self.x % constans.SIDE_OF_BOX == 0 and self.y % constans.SIDE_OF_BOX == 0 and self.timer_sleep <= 0:
            self.timer_sleep = 20
            matrix_position = change_nodes((self.x, self.y))

            self.path = a_star((self.x, self.y), target, game_map)
            if len(self.path) > 0:
                next_position = self.path[0]
                if matrix_position == next_position:

                    if len(self.path) > 1:
                        next_position = self.path[1]
                    else:
                        return 1
                delta = (-matrix_position[0] + next_position[0],
                         -matrix_position[1] + next_position[1])

                delta_arr = self.move_sides.items()
                new_side = 'left'
                for item in delta_arr:
                    if item[1] == delta:
                        new_side = item[0]
                        break

                self.current_side = new_side
                self.last_x = self.x
                self.last_y = self.y
        # base_class.BaseSprite.move(self)

    def check_path_for_directness(self, path):
        if len(path) == 0:
            return False

        (x, y) = path[0]
        direction = None
        for i in range(1, len(path)):
            if path[i][0] == x and (direction is None or direction == 'horizontal'):
                direction = 'horizontal'
            elif path[i][1] == y and (direction is None or direction == 'vertical'):
                direction = 'vertical'
            else:
                return False

        return True

    def check_if_tank_on_line(self, enemy, game_map):
        matrix_x, matrix_y = change_nodes((self.x, self.y))
        enemy_matrix_x, enemy_matrix_y = change_nodes((enemy.x, enemy.y))
        isVertical = matrix_x - enemy_matrix_x in range(-1, 1)
        isHorizontal = matrix_y - enemy_matrix_y in range(-1, 1)
        nodes = []
        if isHorizontal:
            x_start = min(matrix_x, enemy_matrix_x)
            x_end = max(matrix_x, enemy_matrix_x) + 2
            nodes = [(i, j) for i in range(x_start, x_end)
                     for j in range(matrix_y, matrix_y + 2)]

        if isVertical:
            y_start = min(matrix_y, enemy_matrix_y)
            y_end = max(matrix_y, enemy_matrix_y) + 2

            nodes = [(j, i) for i in range(y_start, y_end)
                     for j in range(matrix_x, matrix_x + 2)]

        if len(nodes) == 0:
            return False
        for node in nodes:
            if game_map[node[1]][node[0]] == constans.STEEL_BOX:
                return False

        last_side = self.current_side
        if isHorizontal:
            if matrix_x < enemy_matrix_x:
                self.current_side = 'right'
            else:
                self.current_side = 'left'
        elif isVertical:
            if matrix_y < enemy_matrix_y:
                self.current_side = 'down'
            else:
                self.current_side = 'up'

        return last_side
