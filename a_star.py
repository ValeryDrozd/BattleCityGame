from check_move_possibility import bottom_if, change_nodes, left_if, right_if, up_if
from math import sqrt


class Node:
    def __init__(self, coord, parent_node=None):
        self.coord = coord
        self.parent_node = parent_node
        self.g = 0
        self.h = 0
        self.f = 0


def euclidean_distance(start_coord, finish_coord):
    return sqrt((start_coord[0]-finish_coord[0])**2) + ((start_coord[1]-finish_coord[1])**2)


def get_path(end_node):
    path = []
    current = end_node
    while current is not None:
        path.append(current.coord)
        current = current.parent_node

    path.reverse()
    return path


def a_star(start_position, end_position, game_map, enemies_coords=[]):
    matrix_start_x, matrix_start_y = change_nodes(start_position)
    matrix_end_x, matrix_end_y = change_nodes(end_position)
    start_node = Node((matrix_start_x, matrix_start_y))
    visited = []
    to_visit = []
    to_visit.append(start_node)
    counter = len(game_map)*len(game_map[0])

    while len(to_visit) != 0 and counter >= 0:
        counter -= 1
        curr_node = to_visit[0]
        curr_index = 0
        for i in range(len(to_visit)):
            if to_visit[i].f < curr_node.f:
                curr_node = to_visit[i]
                curr_index = i

        to_visit.pop(curr_index)
        visited.append(curr_node)

        if curr_node.coord == (matrix_end_x, matrix_end_y):
            return get_path(curr_node)
        (current_x, current_y) = curr_node.coord
        next_nodes = [((current_x - 1, current_y), left_if), ((current_x + 1, current_y), right_if),
                      ((current_x, current_y - 1), up_if), ((current_x, current_y + 1), bottom_if)]

        next_nodes = list(map(lambda item: Node(item[0], curr_node), filter(
            lambda item: item[1](curr_node.coord, game_map),
            next_nodes)))
        for next_node in next_nodes:

            if len([
                visited_neighbor
                for visited_neighbor in visited
                if visited_neighbor.coord == next_node.coord
            ]) > 0:
                continue

            if len([
                enemy
                for enemy in enemies_coords
                if enemy == next_node.coord
            ]) > 0:
                continue

            next_node.g = curr_node.g + 1
            next_node.h = euclidean_distance(next_node.coord, end_position)
            next_node.f = next_node.g + next_node.h

            if len([
                    to_visit_node
                    for to_visit_node in to_visit
                    if to_visit_node.coord == next_node.coord
                    and to_visit_node.g < next_node.g]) > 0:
                continue

            to_visit.append(next_node)

    return []
