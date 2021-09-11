from check_move_possibility import change_nodes, left_if, right_if, up_if, bottom_if


def dfs(start_node, end_node, game_map):
    visited = [[False for i in range(len(game_map[0]))] for j in range(len(game_map))]
    matrix_start_x, matrix_start_y = change_nodes(start_node)
    matrix_end_x, matrix_end_y = change_nodes(end_node)

    stack = [(matrix_start_x, matrix_start_y)]
    while len(stack):
        curr = stack[-1]
        if curr == (matrix_end_x, matrix_end_y):
            return stack
        visited[curr[1]][curr[0]] = True
        (current_x, current_y) = curr
        next_node = [((current_x - 1, current_y), left_if), ((current_x + 1, current_y), right_if),
                     ((current_x, current_y - 1), up_if), ((current_x, current_y + 1), bottom_if)]
        flag = False
        for (node, func) in next_node:
            if func(curr, game_map) and not visited[node[1]][node[0]]:
                stack.append(node)
                flag = True
                break

        if not flag:
            stack.pop()
