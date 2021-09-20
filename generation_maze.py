from random import randint

import constans


def maze(width, height):
    matrix = generate_start_map(width, height)
    visited = [[False for i in range(width)] for j in range(height)]
    current = (0, 0)
    visited[current[1]][current[0]] = True
    stack = [current]

    while len(stack) != 0:
        (current_x, current_y) = current
        next_node = [(current_x - 1, current_y), (current_x + 1, current_y),
                     (current_x, current_y - 1), (current_x, current_y + 1)]
        next_node = list(filter(lambda item: 0 <= item[0] < width and 0 <= item[1] < height
                                             and not visited[item[1]][item[0]], next_node))

        if len(next_node) == 0:
            current = stack.pop()
        else:
            rand_node = next_node[randint(0, len(next_node) - 1)]
            stack.append(rand_node)
            visited[rand_node[1]][rand_node[0]] = True
            matrix = break_wall(matrix, current, rand_node)
            current = rand_node

    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == constans.FREE_BOX and randint(0, 100) > 80:
                matrix[i][j] = constans.BRICK_BOX

    for i in range(1, len(matrix) - 1):
        for j in range(1, len(matrix[0]) - 1):
            if matrix[i][j] == constans.STEEL_BOX and randint(0, 100) > 90:
                matrix[i][j] = constans.FREE_BOX
                matrix[i][j + 1] = constans.FREE_BOX

    return matrix


def break_wall(matrix, start_node, target_node):
    real_start_node = (start_node[0] * 3 + 1, start_node[1] * 3 + 1)
    delta = (target_node[0] - start_node[0], target_node[1] - start_node[1])
    if delta[0] == -1:
        matrix[real_start_node[1]][real_start_node[0] - 1] = constans.FREE_BOX
        matrix[real_start_node[1] + 1][real_start_node[0] - 1] = constans.FREE_BOX
    elif delta[0] == 1:
        matrix[real_start_node[1]][real_start_node[0] + 2] = constans.FREE_BOX
        matrix[real_start_node[1] + 1][real_start_node[0] + 2] = constans.FREE_BOX

    elif delta[1] == -1:
        matrix[real_start_node[1] - 1][real_start_node[0]] = constans.FREE_BOX
        matrix[real_start_node[1] - 1][real_start_node[0] + 1] = constans.FREE_BOX
    elif delta[1] == 1:
        matrix[real_start_node[1] + 2][real_start_node[0]] = constans.FREE_BOX
        matrix[real_start_node[1] + 2][real_start_node[0] + 1] = constans.FREE_BOX

    return matrix


def generate_start_map(width, height):
    matrix = []
    real_width = width * 3 + 1
    real_height = height * 3 + 1
    for i in range(real_height):
        delta = []
        for j in range(real_width):
            if i % 3 == 0 or j % 3 == 0:
                delta.append(constans.STEEL_BOX)
                continue

            delta.append(constans.FREE_BOX)

        matrix.append(delta)

    start_position = (1, 1)
    matrix = fill_character_position(matrix, start_position, constans.PLAYER_TANK_BOX)
    spawn_positions = [(len(matrix[0]) - 3, 1), (len(matrix[0]) - 3, len(matrix[1]) - 3)]
    # base_position = (1, 1)
    # matrix[base_position[1]][base_position[0]] = constans.BASE_BOX
    for i in range(len(spawn_positions)):
        matrix = fill_character_position(matrix, spawn_positions[i], constans.ENEMY_TANK_BOX)

    return matrix


def fill_character_position(matrix, position, number):
    matrix[position[1]][position[0]] = number
    matrix[position[1]][position[0] + 1] = number
    matrix[position[1] + 1][position[0]] = number
    matrix[position[1] + 1][position[0] + 1] = number
    return matrix
