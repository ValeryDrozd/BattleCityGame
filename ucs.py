from check_move_possibility import change_nodes, left_if, up_if, right_if, bottom_if
from queue import PriorityQueue


def ucs(start_node, end_node, game_map):
    visited = [[False for i in range(len(game_map[0]))] for j in range(len(game_map))]
    matrix_start_x, matrix_start_y = change_nodes(start_node)
    matrix_end_x, matrix_end_y = change_nodes(end_node)

    queue = PriorityQueue()
    queue.put((0, (matrix_start_x, matrix_start_y), [(matrix_start_x, matrix_start_y)]))

    while not queue.empty():
        length, curr, way = queue.get()
        visited[curr[1]][curr[0]] = True

        if curr == (matrix_end_x, matrix_end_y):
            return way

        (current_x, current_y) = curr
        next_node = [((current_x - 1, current_y), left_if), ((current_x + 1, current_y), right_if),
                     ((current_x, current_y - 1), up_if), ((current_x, current_y + 1), bottom_if)]
        for (node, func) in next_node:
            if func(curr, game_map) and not visited[node[1]][node[0]]:
                queue.put((length + 1, node, way + [node]))

