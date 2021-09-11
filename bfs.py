from check_move_possibility import left_if, right_if, up_if, bottom_if, change_nodes


def get_way(my_dict, node):
    result = [node]
    curr = my_dict[node]
    while curr is not None:
        result.insert(0, curr)
        curr = my_dict[curr]

    return result


def bfs(start_node, end_node, game_map):
    visited = [[False for i in range(len(game_map[0]))] for j in range(len(game_map))]
    matrix_start_x, matrix_start_y = change_nodes(start_node)
    matrix_end_x, matrix_end_y = change_nodes(end_node)

    queue = [(matrix_start_x, matrix_start_y)]
    my_dict = {(matrix_start_x, matrix_start_y): None}

    while len(queue):
        current_node = queue.pop(0)
        visited[current_node[1]][current_node[0]] = True
        (current_x, current_y) = current_node
        if current_x == matrix_end_x and current_y == matrix_end_y:
            return get_way(my_dict, (matrix_end_x, matrix_end_y))

        next_node = [((current_x - 1, current_y), left_if), ((current_x + 1, current_y), right_if),
                     ((current_x, current_y - 1), up_if), ((current_x, current_y + 1), bottom_if)]
        next_node = list(filter(
            lambda item: item[1](current_node, game_map),
            next_node))

        for (node, func) in next_node:
            if node not in queue and not visited[node[1]][node[0]]:
                my_dict[node] = current_node
                queue.append(node)
