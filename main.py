import random
from time import sleep

import pygame as pg
import pygame.time
import projectile
import readmap
import constans
import tank
import texturesfile
import spawn

pg.init()
win = pg.display.set_mode(
    (300 + constans.MAP_WIDTH * constans.SIDE_OF_BOX, 10 + constans.MAP_HEIGHT * constans.SIDE_OF_BOX))

isActive: bool = True
timer: int = 0
player_tank = tank.Tank(owner=constans.PLAYER_TANK, x=2 * constans.SIDE_OF_BOX, y=23 * constans.SIDE_OF_BOX)
player_tank.in_move = True
game_field = readmap.read_map()
enemies: list = []
spawns = [spawn.Spawn(y=0, x=50, spawn_timer=100, height=constans.TANK_HEIGHT, width=constans.TANK_WIDTH)]
bullets: list = []
toDestroy: list = []
justSpawned: list = []
amount_all_enemies = 3
current_spawns = 2
score = 0
winner = 0


def checkWin():
    win.fill((255, 255, 255))
    echo("YOU WIN", [400, 250, 400, 400])
    pg.display.update()


def checkLose():
    win.fill((255, 255, 255))
    echo("YOU LOSE", [400, 250, 400, 400])
    pg.display.update()


def spawnEnemies():
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


def echo(text, position):
    font = pygame.font.SysFont('Comic Sans MS', 25)
    text = font.render(text, True, (0, 0, 0))
    win.blit(text, position)


def echoText():
    pygame.draw.rect(win, (255, 255, 255), (constans.MAP_WIDTH * constans.SIDE_OF_BOX + 5, 5, 250, 100))
    pygame.draw.rect(win, (255, 255, 255), (constans.MAP_WIDTH * constans.SIDE_OF_BOX + 5, 5, 250, 100))
    echo("Score: " + str(min(score, 999)), [constans.MAP_WIDTH * constans.SIDE_OF_BOX + 10, 5])
    echo("Enemies: " + str(min(amount_all_enemies, 999)), [constans.MAP_WIDTH * constans.SIDE_OF_BOX + 10, 35])


def process_game():
    global amount_all_enemies
    global winner
    global score
    for enemy in enemies:
        enemy.analyse(collide(enemy))
        if not collide(enemy):
            enemy.move()
        if random.randint(0, 10) == 0:
            shoot(enemy)
    for i in range(len(bullets) - 1, -1, -1):
        t = collide_work(bullets[i])
        if collide(bullets[i]) or t:
            if bullets[i].owner == 1:
                for j in range(len(enemies) - 1, -1, -1):
                    if collide_rects([(bullets[i].x, bullets[i].y),
                                      (bullets[i].x + bullets[i].width, bullets[i].y + bullets[i].height)],
                                     [(enemies[j].x, enemies[j].y),
                                      (enemies[j].x + enemies[j].width, enemies[j].y + enemies[j].height)]):
                        del enemies[j]
                        amount_all_enemies -= 1
                        if amount_all_enemies == 0:
                            winner = 1
                        score += 1
                        echoText()
            else:
                if collide_rects([(bullets[i].x, bullets[i].y),
                                  (bullets[i].x + bullets[i].width, bullets[i].y + bullets[i].height)],
                                 [(player_tank.x, player_tank.y),
                                  (player_tank.x + player_tank.width, player_tank.y + player_tank.height)]):
                    winner = -1
                    break
            if not bullets[i] in justSpawned:
                toDestroy.append((5 + bullets[i].x, 5 + bullets[i].y, bullets[i].width, bullets[i].height))
            else:
                justSpawned.remove(bullets[i])
            del bullets[i]

        else:
            bullets[i].move()


def collide_rects(first, second):
    sprite_left_top = first[0]
    sprite_right_bot = first[1]
    current_left_top = second[0]
    current_right_bot = second[1]
    temp_left_top = sprite_left_top
    temp_right_bot = sprite_right_bot
    if temp_left_top[0] > current_left_top[0]:
        temp_left_top, temp_right_bot, current_left_top, current_right_bot = \
            current_left_top, current_right_bot, temp_left_top, temp_right_bot

    if current_left_top[0] < temp_right_bot[0] and (
            temp_right_bot[1] >= current_left_top[1] >= temp_left_top[1] or
            temp_right_bot[1] >= current_right_bot[1] >= temp_left_top[1]):
        return True
    return False


def collide_tank(sprite: tank.Tank or spawn.Spawn):
    tanks = [player_tank] + enemies
    if isinstance(sprite, tank.Tank) or isinstance(sprite, projectile.Projectile):
        sprite_left_top = (
            sprite.x + sprite.move_sides[sprite.current_side][0], sprite.y + sprite.move_sides[sprite.current_side][1])
        sprite_right_bot = (sprite_left_top[0] + sprite.width, sprite_left_top[1] + sprite.height)
    else:
        sprite_left_top = (sprite.x, sprite.y)
        sprite_right_bot = (sprite_left_top[0] + sprite.width, sprite_left_top[1] + sprite.height)
    is_collision: bool = False
    for current in tanks:
        if current != sprite and collide_rects([sprite_left_top, sprite_right_bot],
                                               [(current.x, current.y),
                                                (current.x + current.width, current.y + current.height)]):
            is_collision = True
            break
    if not is_collision and isinstance(sprite, tank.Tank):
        return collide_work(sprite)
    else:
        return is_collision


def collide_work(sprite):
    global winner
    nx_begin = min(max(0, sprite.x+sprite.move_sides[sprite.current_side][0]*sprite.speed),
                   constans.MAP_WIDTH * constans.SIDE_OF_BOX - sprite.width + 1)//constans.SIDE_OF_BOX
    ny_begin = min(max(0, sprite.y+sprite.move_sides[sprite.current_side][1]*sprite.speed),
                   constans.MAP_WIDTH * constans.SIDE_OF_BOX - sprite.height + 1)//constans.SIDE_OF_BOX
    nx_end = min(max(0, sprite.x+sprite.move_sides[sprite.current_side][0]*sprite.speed + sprite.width - 1),
                 constans.MAP_WIDTH * constans.SIDE_OF_BOX - 1)//constans.SIDE_OF_BOX
    ny_end = min(max(0, sprite.y+sprite.move_sides[sprite.current_side][1]*sprite.speed + sprite.height - 1),
                 constans.MAP_WIDTH * constans.SIDE_OF_BOX - 1)//constans.SIDE_OF_BOX
    isCollision = False
    for i in range(ny_end - ny_begin + 1):
        for j in range(nx_end - nx_begin + 1):
            if game_field[ny_begin + i][nx_begin + j] in {constans.BRICK_BOX, constans.STEEL_BOX}:
                isCollision = True
                if not isinstance(sprite, projectile.Projectile):
                    break
            if game_field[ny_begin + i][nx_begin + j] == constans.BRICK_BOX and\
                    isinstance(sprite, projectile.Projectile):
                toDestroy.append((5 + (nx_begin + j) * constans.SIDE_OF_BOX,
                                  5 + (ny_begin + i) * constans.SIDE_OF_BOX,
                                  constans.SIDE_OF_BOX, constans.SIDE_OF_BOX))
                game_field[ny_begin + i][nx_begin + j] = 0
                isCollision = True
                break
            elif game_field[ny_begin + i][nx_begin + j] == constans.BASE_BOX:
                winner = -1
    return isCollision


def colliding_edges(sprite):
    if (sprite.current_side == 'left' and sprite.x <= 0) or \
       (sprite.current_side == 'up' and sprite.y <= 0) or \
       (sprite.current_side == 'down' and sprite.y + sprite.height >= constans.MAP_HEIGHT * constans.SIDE_OF_BOX) or \
       (sprite.current_side == 'right' and sprite.x + sprite.width >= constans.MAP_WIDTH * constans.SIDE_OF_BOX):
        return True
    return False


def collide(sprite):
    global winner
    res = colliding_edges(sprite) or collide_work(sprite) or collide_tank(sprite)
    if res and isinstance(sprite, tank.Tank):
        winner = 0
    return res


def get_destroyable():
    global toDestroy
    toDestroy = [(5 + player_tank.x, 5 + player_tank.y, player_tank.width, player_tank.height)]
    for enemy in enemies:
        toDestroy.append((5 + enemy.x, 5 + enemy.y, enemy.width, enemy.height))
    for bullet in bullets:
        toDestroy.append((5 + bullet.x, 5 + bullet.y, bullet.width, bullet.height))


def initial_draw():
    win.fill((255, 255, 255))
    echoText()
    pg.draw.rect(win, constans.BACKGROUND_COLOR,
                 (5, 5, constans.SIDE_OF_BOX * constans.MAP_WIDTH, constans.SIDE_OF_BOX * constans.MAP_HEIGHT))
    for i in range(constans.MAP_HEIGHT):
        for j in range(constans.MAP_WIDTH):
            if game_field[i][j] != 0:
                win.blit(texturesfile.TEXTURES_DICT[game_field[i][j]],
                         (5 + constans.SIDE_OF_BOX * j, 5 + constans.SIDE_OF_BOX * i))


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

    win.blit(player_tank.textures[player_tank.current_side], (5 + player_tank.x, 5 + player_tank.y))
    for enemy in enemies:
        win.blit(enemy.textures[enemy.current_side], (5 + enemy.x, 5 + enemy.y))

    for bullet in bullets:
        win.blit(bullet.textures[bullet.current_side], (5 + bullet.x, 5 + bullet.y))


def toEdge(sprite):
    left = 0
    t = right = sprite.speed
    while right - left != 1:
        mid = (right + left) // 2
        sprite.speed = mid
        if collide(sprite):
            left = mid
        else:
            right = mid

    sprite.speed = left
    sprite.move()
    sprite.speed = t


initial_draw()
draw_game()
while isActive:
    if winner == 1:
        checkWin()
        pygame.time.delay(3000)
        break
    elif winner == -1:
        checkLose()
        pygame.time.delay(3000)
        break
    pygame.time.delay(constans.UPDATE_TIME)
    get_destroyable()
    if amount_all_enemies > 0:
        spawnEnemies()
    timer += constans.UPDATE_TIME

    for event in pg.event.get():
        if event.type == pg.QUIT:
            isActive = False

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        player_tank.current_side = 'left'
        if not collide_work(player_tank):
            player_tank.move()
        else:
            toEdge(player_tank)
    elif keys[pg.K_RIGHT]:
        player_tank.current_side = 'right'
        if not collide_tank(player_tank):
            player_tank.move()
        else:
            toEdge(player_tank)
    elif keys[pg.K_UP]:
        player_tank.current_side = 'up'
        if not collide_tank(player_tank):
            player_tank.move()
        else:
            toEdge(player_tank)
    elif keys[pg.K_DOWN]:
        player_tank.current_side = 'down'
        if not collide_tank(player_tank):
            player_tank.move()
        else:
            toEdge(player_tank)
    elif keys[pg.K_SPACE]:
        shoot(player_tank)
    process_game()
    draw_game()
    pg.display.update()


pygame.quit()
