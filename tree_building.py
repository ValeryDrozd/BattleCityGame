
import math

from minimax import FieldState, Node
from check_move_possibility import left_if, right_if, up_if, bottom_if, change_nodes


def evaluate(node: Node, target: tuple[int, int]):
    enemy_distance = math.inf
    player_coord = node.state.get_player_position()
    if target == player_coord:
        return -math.inf
    enemies_coords = node.state.get_enemies_positions()

    for enemy in enemies_coords:
        distance = math.sqrt(math.pow(
            enemy[0] - player_coord[0], 2) + math.pow(enemy[1] - player_coord[1], 2))
        if enemy_distance is None or enemy_distance > distance:
            enemy_distance = distance
    target_distance = math.sqrt(math.pow(
        target[0] - player_coord[0], 2) + math.pow(target[1] - player_coord[1], 2))
    output = -(target_distance + enemy_distance)/2

    return output


def tree_build(start_state: FieldState, target):
    start_node = Node(start_state, None)
    tree_build_recursive(start_node, 1, start_state.matrix, target)
    return start_node


def tree_build_recursive(current_node: Node, depth, game_map, target):
    if depth > 5:
        current_node.value = evaluate(current_node, target)
        return None
    curr_state = current_node.state
    player_coord = curr_state.get_player_position()
    enemies_coords = curr_state.get_enemies_positions()
    if depth % 2 == 1:
        (current_x, current_y) = player_coord
        neighboring_nodes = list(filter(
            lambda item: item[1](player_coord, game_map),
            [((current_x - 1, current_y), left_if), ((current_x + 1, current_y), right_if),
             ((current_x, current_y - 1), up_if), ((current_x, current_y + 1), bottom_if)]
        ))
        neighboring_nodes = list(filter(
            lambda x: x not in enemies_coords, neighboring_nodes))

        new_nodes = list(map(lambda node: Node(curr_state.change_character_position(
            player_coord, node[0], 0), None), neighboring_nodes))
        
        # print('Build pos: ' + str(current_node.state.get_player_position()))
        # print("Poss nodes")
        # for node in new_nodes:
            # print(node.state.get_player_position())
        current_node.children = new_nodes

    else:

        neighboring_nodes = []
        # get_neighbors(
        # curr_state.matrix, coord) for coord in enemies_coords]
        for coord in enemies_coords:
            (current_x, current_y) = coord
            next_node = list(filter(
                lambda item: item[1](coord, game_map),
                [((current_x - 1, current_y), left_if), ((current_x + 1, current_y), right_if),
                 ((current_x, current_y - 1), up_if), ((current_x, current_y + 1), bottom_if)]))
            neighboring_nodes.append(list(map(lambda x: x[0], next_node)))
        variations = get_variations(neighboring_nodes)
        new_nodes = []
        for variant in variations:
            if player_coord in variant:
                continue
            state = curr_state
            for i in range(len(enemies_coords)):
                state = state.change_character_position(
                    enemies_coords[i], variant[i], game_map[enemies_coords[i][1]][enemies_coords[i][0]])

            new_nodes.append(Node(state, None))
        current_node.children = new_nodes
    for child in current_node.children:
        tree_build_recursive(child, depth+1, game_map, target)


def get_variations(arr):
    result = []

    def get_variations_recurs(last_arr, res):
        if len(last_arr) == 0:
            result.append(res)
            return
        curr_arr = last_arr[0]
        for item in curr_arr:
            get_variations_recurs(last_arr[1:], res + [item])
    get_variations_recurs(arr, [])
    return result
