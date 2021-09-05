import pygame as pg
import pygame.time
import readmap
import constans
import tank
import texturesfile

pg.init()
win = pg.display.set_mode(
    (10 + constans.MAP_WIDTH * constans.SIDE_OF_BOX, 10 + constans.MAP_HEIGHT * constans.SIDE_OF_BOX))

isActive: bool = True
timer: int = 0
player_tank = tank.Tank(owner=constans.PLAYER_TANK, x=0, y=0)
player_tank.in_move = True
game_field = readmap.read_map()
enemies: list = []


def processGame():
    for enemy in enemies:
        enemy.analyse()


def drawGame():
    win.fill((255, 255, 255))
    pg.draw.rect(win, (0, 0, 0),
                 (5, 5, constans.SIDE_OF_BOX * constans.MAP_WIDTH, constans.SIDE_OF_BOX * constans.MAP_HEIGHT))
    for i in range(constans.MAP_HEIGHT):
        for j in range(constans.MAP_WIDTH):
            if game_field[i][j] != 0:
                win.blit(texturesfile.TEXTURES_DICT[game_field[i][j]],
                         (5 + constans.SIDE_OF_BOX * j, 5 + constans.SIDE_OF_BOX * i))


while isActive:
    pygame.time.delay(constans.UPDATE_TIME)
    timer += constans.UPDATE_TIME

    for event in pg.event.get():
        if event.type == pg.QUIT:
            isActive = False

    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        player_tank.current_side = 'left'
        player_tank.move()
    elif keys[pg.K_RIGHT]:
        player_tank.current_side = 'right'
    elif keys[pg.K_UP]:
        player_tank.current_side = 'up'
    elif keys[pg.K_DOWN]:
        player_tank.current_side = 'down'
    elif keys[pg.K_SPACE]:
        player_tank.shoot()

    processGame()
    drawGame()
    pg.display.update()

pygame.quit()
