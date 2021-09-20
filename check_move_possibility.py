from math import floor
import constans


def check(item, game_map):
    return 0 <= item[0] < len(game_map[0]) \
           and 0 <= item[1] < len(game_map) \
           and (game_map[item[1]][item[0]] == 0 or game_map[item[1]][item[0]] == 1)


def left_if(node, game_map):
    arr = [(node[0] - 1, node[1]), (node[0] - 1, node[1] + 1)]
    return all(list(map(lambda x: check(x, game_map), arr)))


def right_if(node, game_map):
    return all(list(map(lambda x: check(x, game_map),
                        [(node[0] + 2, node[1]), (node[0] + 2, node[1] + 1)])))


def up_if(node, game_map):
    return all(list(map(lambda x: check(x, game_map),
                        [(node[0], node[1] - 1), (node[0] + 1, node[1] - 1)])))


def bottom_if(node, game_map):
    return all(list(map(lambda x: check(x, game_map),
                        [(node[0], node[1] + 2), (node[0] + 1, node[1] + 2)])))


def change_nodes(node):
    (x, y) = node
    return round(x / constans.SIDE_OF_BOX), round(y / constans.SIDE_OF_BOX)
