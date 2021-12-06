from dqn_tank import DQN_Tank
from main import start_game
import pygame as pg
import constans


def loop():
    pg.init()
    win = pg.display.set_mode(
        (constans.MAP_WIDTH * constans.SIDE_OF_BOX, constans.MAP_HEIGHT * constans.SIDE_OF_BOX))
    steps = 6856
    for i in range(1000):
        player_tank = DQN_Tank(owner=constans.PLAYER_TANK, x=1 * constans.SIDE_OF_BOX,
                               y=1 * constans.SIDE_OF_BOX)
        player_tank.initVariables()
        player_tank.total_steps_count = steps
        (winner, time, tank) = start_game(win, player_tank)
        steps += tank.current_steps_count
        file = open('.log', "a")
        file.write("Winner: " + str(winner) + ", time: " + str(time) + " steps: " + str(tank.current_steps_count) + " total steps: " +
                   str(steps) + " reward: " + str(tank.total_reward) + " epsilon: " + str(tank.params["eps"]) + " Q-parameter: " + str(max(tank.Q_parameters, default=float('nan'))) + "\n")

    pg.quit()


loop()
