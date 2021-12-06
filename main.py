from a_star import a_star
import random
import time
from time import sleep

import pygame as pg
import pygame.time
from copy import deepcopy

import generation_maze
import projectile
import constans
from readmap import read_map
import tank
import texturesfile
import spawn
from bfs import bfs
from check_move_possibility import change_nodes
from dfs import dfs
from ucs import ucs

from dqn_tank import DQN_Tank


def track_time(lam):
    start = time.time()
    output = lam()
    return output, time.time() - start


def collide_rects(first, second):
    [first, second] = sorted([first, second], key=lambda a: a[0][0])
    first_left_top = first[0]
    first_right_bot = first[1]
    second_left_top = second[0]
    second_right_bot = second[1]
    aLeftOfB = first_right_bot[0] < second_left_top[0]
    aRightOfB = first_left_top[0] > second_right_bot[0]
    aAboveB = first_left_top[1] > second_right_bot[1]
    aBelowB = first_right_bot[1] < second_left_top[1]

    return not (aLeftOfB or aRightOfB or aAboveB or aBelowB)


def colliding_edges(sprite):
    if (sprite.current_side == 'left' and sprite.x <= 0) or \
            (sprite.current_side == 'up' and sprite.y <= 0) or \
            (
        sprite.current_side == 'down' and sprite.y + sprite.height >= constans.MAP_HEIGHT * constans.SIDE_OF_BOX) or \
            (sprite.current_side == 'right' and sprite.x + sprite.width >= constans.MAP_WIDTH * constans.SIDE_OF_BOX):
        return True
    return False


bullets: list = []
toDestroy: list = []
justSpawned: list = []
amount_all_enemies = 1
current_spawns = 1
score = 0
winner = 0
timer: int = 0
isActive: bool = True


def start_game(win, player_tank: DQN_Tank):
    global timer
    global isActive
    global bullets
    global toDestroy
    global justSpawned
    global amount_all_enemies
    global current_spawns
    global score
    global winner
    global timer
    global isActive

    bullets = []
    toDestroy = []
    justSpawned = []
    amount_all_enemies = 3
    current_spawns = 2
    score = 0
    winner = 0
    timer = 0
    isActive = True

    # game_field = generation_maze.maze(8, 8)
    game_field = read_map()
    start_tank_position = None
    spawn_positions = []

    for i in range(len(game_field)):
        for j in range(len(game_field[0])):
            if game_field[i][j] == 4 and start_tank_position is None:
                start_tank_position = (j, i)
            elif game_field[i][j] == 5 and game_field[i + 1][j + 1] == 5:
                spawn_positions.append((j, i))

    for i in range(len(game_field)):
        for j in range(len(game_field[0])):
            if game_field[i][j] == 4 or game_field[i][j] == 5:
                game_field[i][j] = 0

    player_tank.x = start_tank_position[0]*constans.SIDE_OF_BOX
    player_tank.y = start_tank_position[1]*constans.SIDE_OF_BOX
    player_tank.in_move = True
    # game_field = readmap.read_map()
    enemies: list = []

    spawns = [spawn.Spawn(y=spawn_position[1] * constans.SIDE_OF_BOX, x=spawn_position[0] * constans.SIDE_OF_BOX,
                          spawn_timer=1000, height=constans.TANK_HEIGHT,
                          width=constans.TANK_WIDTH) for spawn_position in spawn_positions]
    # bullets: list = []
    # toDestroy: list = []
    # justSpawned: list = []
    # amount_all_enemies = 3
    # current_spawns = 2
    # score = 0
    # winner = 0

    def spawn_enemies():
        global amount_all_enemies
        global timer
        if min(current_spawns, amount_all_enemies) <= len(enemies):
            return
        available_spawns = [i for i in range(len(spawns)) if
                            (not collide_tank(spawns[i]) and (timer - spawns[i].last_spawn >= spawns[i].spawn_timer))]
        if len(available_spawns) == 0:
            return
        current_spawn: int = random.choice(available_spawns)
        enemies.append(spawns[current_spawn].getTank())
        spawns[current_spawn].last_spawn = timer
        enemies[-1].in_move = True

    way_mode = constans.A_STAR

    def process_game():
        global amount_all_enemies
        global winner
        global score
        for enemy in enemies:
            # enemy.analyse(collide(enemy))
            if not collide(enemy):
                enemy.move()
            # if random.randint(0, 10) == 0:
            #     shoot(enemy)
        for i in range(len(bullets) - 1, -1, -1):
            t = collide_work(bullets[i])
            if collide(bullets[i]) or t != 0:
                if bullets[i].owner == 1:
                    for j in range(len(enemies) - 1, -1, -1):
                        check = collide_rects([(bullets[i].x, bullets[i].y),
                                               (bullets[i].x + bullets[i].width, bullets[i].y + bullets[i].height)],
                                              [(enemies[j].x, enemies[j].y),
                                               (enemies[j].x + enemies[j].width, enemies[j].y + enemies[j].height)])
                        if check:
                            enemies[j].hp -= 1
                            if enemies[j].hp == 0:
                                del enemies[j]
                                amount_all_enemies -= 1
                                if amount_all_enemies == 0:
                                    winner = 1
                                player_tank.score += 300
                else:
                    if collide_rects([(bullets[i].x, bullets[i].y),
                                      (bullets[i].x + bullets[i].width, bullets[i].y + bullets[i].height)],
                                     [(player_tank.x, player_tank.y),
                                      (player_tank.x + player_tank.width, player_tank.y + player_tank.height)]):
                        player_tank.hp -= 1
                        if player_tank.hp == 0:
                            winner = -1
                            player_tank.score -= 100
                if not bullets[i] in justSpawned:
                    toDestroy.append(
                        (bullets[i].x, bullets[i].y, bullets[i].width, bullets[i].height))
                else:
                    justSpawned.remove(bullets[i])
                del bullets[i]

            else:
                bullets[i].move()

    def collide_tank(sprite: tank.Tank or spawn.Spawn):
        tanks = [player_tank] + enemies
        if isinstance(sprite, tank.Tank) or isinstance(sprite, projectile.Projectile):
            sprite_left_top = (
                sprite.x + sprite.move_sides[sprite.current_side][0], sprite.y + sprite.move_sides[sprite.current_side][1])
            sprite_right_bot = (
                sprite_left_top[0] + sprite.width, sprite_left_top[1] + sprite.height)
        else:
            sprite_left_top = (sprite.x, sprite.y)
            sprite_right_bot = (
                sprite_left_top[0] + sprite.width, sprite_left_top[1] + sprite.height)
        is_collision: bool = False
        for current in tanks:
            if current != sprite and collide_rects([sprite_left_top, sprite_right_bot],
                                                   [(current.x, current.y),
                                                    (current.x + current.width, current.y + current.height)]):
                is_collision = True
                break
        if not is_collision and isinstance(sprite, tank.Tank):
            return collide_work(sprite) != 0
        else:
            return is_collision

    def collide_work(sprite):
        global winner
        nx_begin = min(max(0, sprite.x + sprite.move_sides[sprite.current_side][0] * sprite.speed),
                       constans.MAP_WIDTH * constans.SIDE_OF_BOX - sprite.width + 1) // constans.SIDE_OF_BOX
        ny_begin = min(max(0, sprite.y + sprite.move_sides[sprite.current_side][1] * sprite.speed),
                       constans.MAP_WIDTH * constans.SIDE_OF_BOX - sprite.height + 1) // constans.SIDE_OF_BOX
        nx_end = min(max(0, sprite.x + sprite.move_sides[sprite.current_side][0] * sprite.speed + sprite.width - 1),
                     constans.MAP_WIDTH * constans.SIDE_OF_BOX - 1) // constans.SIDE_OF_BOX
        ny_end = min(max(0, sprite.y + sprite.move_sides[sprite.current_side][1] * sprite.speed + sprite.height - 1),
                     constans.MAP_WIDTH * constans.SIDE_OF_BOX - 1) // constans.SIDE_OF_BOX

        is_collision = 0
        for i in range(ny_end - ny_begin + 1):
            for j in range(nx_end - nx_begin + 1):
                if game_field[ny_begin + i][nx_begin + j] in {constans.BRICK_BOX, constans.STEEL_BOX}:
                    is_collision = 1
                    if not isinstance(sprite, projectile.Projectile):
                        break
                if game_field[ny_begin + i][nx_begin + j] == constans.BRICK_BOX and \
                        isinstance(sprite, projectile.Projectile):
                    toDestroy.append(((nx_begin + j) * constans.SIDE_OF_BOX,
                                      (ny_begin + i) * constans.SIDE_OF_BOX,
                                      constans.SIDE_OF_BOX, constans.SIDE_OF_BOX))
                    game_field[ny_begin + i][nx_begin + j] = 0
                    is_collision = constans.BRICK_BOX
                    break
                elif game_field[ny_begin + i][nx_begin + j] == constans.BASE_BOX:
                    winner = -1
        return is_collision

    def collide(sprite):
        global winner
        res = colliding_edges(sprite) or (collide_work(
            sprite) != 0) or collide_tank(sprite)
        if res and isinstance(sprite, tank.Tank):
            winner = 0
        return res

    def get_destroyable():
        global toDestroy
        toDestroy = [(player_tank.x, player_tank.y,
                      player_tank.width, player_tank.height)]
        for enemy in enemies:
            toDestroy.append((enemy.x, enemy.y, enemy.width, enemy.height))
        for bullet in bullets:
            toDestroy.append((bullet.x, bullet.y, bullet.width, bullet.height))

    def initial_draw():
        win.fill((255, 255, 255))
        pg.draw.rect(win, constans.BACKGROUND_COLOR,
                     (0, 0, constans.SIDE_OF_BOX * constans.MAP_WIDTH, constans.SIDE_OF_BOX * constans.MAP_HEIGHT))
        for i in range(constans.MAP_HEIGHT):
            for j in range(constans.MAP_WIDTH):
                if game_field[i][j] != 0 and game_field[i][j] != 4 and game_field[i][j] != 5:
                    win.blit(texturesfile.TEXTURES_DICT[game_field[i][j]],
                             (constans.SIDE_OF_BOX * j, constans.SIDE_OF_BOX * i))

    def shoot(sprite):
        curr_bullet = sprite.shoot()
        if timer - sprite.last_shot >= sprite.reload_time and not colliding_edges(curr_bullet):
            bullets.append(curr_bullet)
            justSpawned.append(bullets[-1])
            sprite.last_shot = timer

    def draw_game():
        global toDestroy
        for destroyable in toDestroy:
            pg.draw.rect(win, constans.BACKGROUND_COLOR,
                         destroyable)

        win.blit(
            player_tank.textures[player_tank.current_side], (player_tank.x, player_tank.y))
        for enemy in enemies:
            win.blit(enemy.textures[enemy.current_side], (enemy.x, enemy.y))

        for bullet in bullets:
            win.blit(bullet.textures[bullet.current_side],
                     (bullet.x, bullet.y))

    last_ways = []
    colors = [(random.randint(0, 255), random.randint(
        0, 255), random.randint(0, 255)) for i in range(5)]

    def draw_way(ways):
        # if last_ways:
        for last_way in last_ways:
            for (lx, ly) in last_way:
                possible_brick_nodes = [
                    (lx, ly), (lx + 1, ly), (lx, ly + 1), (lx + 1, ly + 1)]
                for (x, y) in possible_brick_nodes:
                    real_x, real_y = x * constans.SIDE_OF_BOX, y * constans.SIDE_OF_BOX
                    if game_field[y][x] == constans.FREE_BOX:
                        pg.draw.rect(win, constans.BACKGROUND_COLOR,
                                     (real_x, real_y, constans.SIDE_OF_BOX,
                                      constans.SIDE_OF_BOX))

        if ways:
            for i in range(len(ways)):
                way = ways[i]
                color = colors[i]
                for (x, y) in way:
                    real_x, real_y = x * constans.SIDE_OF_BOX, y * constans.SIDE_OF_BOX
                    surface = pg.Surface((constans.TANK_WIDTH,
                                          constans.TANK_WIDTH))
                    surface.fill(color)
                    surface.set_alpha(50)
                    win.blit(surface, (real_x, real_y))
                    possible_brick_nodes = [
                        (x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1)]
                    for node in possible_brick_nodes:
                        if game_field[node[1]][node[0]] == constans.BRICK_BOX:
                            win.blit(texturesfile.TEXTURES_DICT[constans.BRICK_BOX],
                                     (constans.SIDE_OF_BOX * node[0], constans.SIDE_OF_BOX * node[1]))

    def toEdge(sprite):
        left = 0
        t = right = sprite.speed
        while right - left != 1:
            mid = (right + left) // 2
            sprite.speed = mid
            if collide(sprite) != 0:
                left = mid
            else:
                right = mid

        sprite.speed = left
        sprite.move()
        sprite.speed = t

    initial_draw()
    draw_game()

    target = (10 * constans.SIDE_OF_BOX, 10 * constans.SIDE_OF_BOX)

    while isActive:
        if winner == 1:
            break
        elif winner == -1:
            break
        pygame.time.delay(constans.UPDATE_TIME - 10)
        get_destroyable()
        if amount_all_enemies > 0:
            spawn_enemies()
        timer += constans.UPDATE_TIME

        for event in pg.event.get():
            if event.type == pg.QUIT:
                isActive = False

        if len(enemies) != 0 and timer % (constans.UPDATE_TIME * 6) == 0:
            choices = {constans.BFS: bfs, constans.DFS: dfs,
                       constans.UCS: ucs, constans.A_STAR: a_star}
            # way_func = choices.get(way_mode)
            # results = track_time(
            #     lambda: list(map(lambda enemy: way_func((player_tank.x, player_tank.y), (enemy.x, enemy.y), game_field),
            #                      enemies)))
            # print(results[0])
            # print_way_info(results)
            # draw_way(results[0])
            # last_ways = results[0]

        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_RIGHT] or keys[pg.K_UP] or keys[pg.K_DOWN]:
            arrows = {pg.K_LEFT: 'left', pg.K_RIGHT: 'right',
                      pg.K_UP: 'up', pg.K_DOWN: 'down'}
            for key in arrows:
                if keys[key]:
                    player_tank.current_side = arrows[key]

            if not collide(player_tank):
                player_tank.move()
            else:
                toEdge(player_tank)

        if collide_work(player_tank) == constans.BRICK_BOX:
            shoot(player_tank)

        for enemy in enemies:
            enemy.auto_move(game_field, (player_tank.x, player_tank.y))

        # check = player_tank.auto_move(game_field, target)
        # if check == 1:
        #     target = (
        #         (random.randint(0, 7) * 3 + 1) * constans.SIDE_OF_BOX,
        #         (random.randint(0, 7) * 3 + 1) * constans.SIDE_OF_BOX)

        copy_game_field = deepcopy(game_field)
        player_tank_pos = change_nodes((player_tank.x, player_tank.y))
        enemies_pos = list(map(lambda x: change_nodes((x.x, x.y)), enemies))

        def set_character_in_map(game_map, positions, symbol):
            for pos in positions:
                game_map[pos[1]][pos[0]] = symbol
        
        set_character_in_map(copy_game_field, [player_tank_pos], constans.PLAYER_TANK_BOX)
        set_character_in_map(copy_game_field, enemies_pos, constans.ENEMY_TANK_BOX)


        player_tank.dqn_get_choice(copy_game_field, list(map(lambda x: (x.x, x.y), enemies)))

        for enemy in enemies:
            enemy_check = enemy.check_if_tank_on_line(player_tank, game_field)
            if collide_work(enemy) == constans.BRICK_BOX:
                shoot(enemy)
            if enemy_check:
                shoot(enemy)
                enemy.current_side = enemy_check
            check = player_tank.check_if_tank_on_line(enemy, game_field)
            if check:  # or collide_work(player_tank) == constans.BRICK_BOX:
                shoot(player_tank)
                player_tank.current_side = check

        if collide(player_tank) == 0:
            player_tank.move()
        else:
            toEdge(player_tank)
        result = player_tank.path

        draw_way([result])
        last_ways = [result]

        if keys[pg.K_SPACE]:
            shoot(player_tank)
        if keys[pg.K_z]:
            way_mode += 1
            if way_mode > constans.A_STAR:
                way_mode = constans.BFS
            sleep(0.1)

        process_game()
        draw_game()
        pg.display.update()

    player_tank.do_training_step(game_field, list(map(lambda x: (x.x, x.y), enemies)), last_game_step=True)
    return (winner, timer, player_tank)
