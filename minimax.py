
import math
from copy import deepcopy
import constans


class FieldState:
    def __init__(self, matrix, score=0) -> None:
        self.matrix = matrix
        self.score = score

    def __str__(self) -> str:
        return '\n'.join([str(line) for line in self.matrix])

    def get_player_position(self):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                if self.matrix[i][j] == constans.PLAYER_TANK_BOX:
                    return (j, i)

    def get_enemies_positions(self):
        coords = []
        for i in range(1, len(self.matrix) - 1):
            for j in range(1, len(self.matrix[0]) - 1):
                if self.matrix[i][j] == constans.ENEMY_TANK_BOX and \
                        self.matrix[i+1][j] == constans.ENEMY_TANK_BOX and \
                        self.matrix[i][j+1] == constans.ENEMY_TANK_BOX and \
                        self.matrix[i+1][j+1] == constans.ENEMY_TANK_BOX:
                    coords.append((j, i))
        return coords

    def change_character_position(self, coord, new_coord, new_value_on_last_coord):
        new_matrix = deepcopy(self.matrix)
        character_number = new_matrix[coord[1]][coord[0]]
        new_matrix[coord[1]][coord[0]] = new_value_on_last_coord
        new_matrix[coord[1]][coord[0] + 1] = new_value_on_last_coord
        new_matrix[coord[1] + 1][coord[0]] = new_value_on_last_coord
        new_matrix[coord[1] + 1][coord[0] + 1] = new_value_on_last_coord
        new_matrix[new_coord[1]][new_coord[0]] = character_number
        new_matrix[new_coord[1]+1][new_coord[0]] = character_number
        new_matrix[new_coord[1]][new_coord[0]+1] = character_number
        new_matrix[new_coord[1]+1][new_coord[0]+1] = character_number
        new_score = self.score

        return FieldState(new_matrix, new_score)


class Node:
    def __init__(self, state: FieldState, value) -> None:
        self.state = state
        self.value = value
        self.children: list[Node] = []

    def __str__(self) -> str:
        output = str(self.state) + " " + str(self.value) + "\n"
        strings = '\n'.join(map(lambda x: '\n'.join(
            map(lambda y: "   " + y, str(x).split('\n'))), self.children))
        output += '{\n' + strings + '}\n' if strings != '' else ''
        return output


def minimax(curr_node: Node, alpha, beta, depth):
    is_max = depth % 2 == 0
    if len(curr_node.children) == 0:
        return curr_node.value

    if is_max:
        best_value = -math.inf
        for child in curr_node.children:
            value = minimax(child, alpha, beta, depth+1)
            best_value = max(
                best_value, value) if value is not None else best_value
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        curr_node.value = best_value
        return best_value

    else:
        best_value = math.inf
        for child in curr_node.children:
            value = minimax(child, alpha, beta, depth+1)
            best_value = min(
                best_value, value) if value is not None else best_value
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        curr_node.value = best_value
        return best_value


def expectimax(curr_node: Node, depth):
    is_max = depth % 2 == 0
    if len(curr_node.children) == 0:
        return curr_node.value

    if is_max:
        best_value = -math.inf
        for child in curr_node.children:
            value = expectimax(child, depth+1)
            best_value = max(
                best_value, value) if value is not None else best_value
        curr_node.value = best_value
        return best_value

    else:
        values = 0
        for child in curr_node.children:
            value = expectimax(child, depth+1)
            values += value if value is not None else 0
        curr_node.value = values / len(curr_node.children)
        return curr_node.value
