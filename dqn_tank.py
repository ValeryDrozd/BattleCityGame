import math
import random
from dqn import DQN
from tank import Tank
import numpy as np
import constans
import tensorflow as tf
from time import time, strftime, localtime
from collections import deque


dqn_params = {
    "width": constans.MAP_WIDTH,
    "height": constans.MAP_HEIGHT,
    "num_training": 10000,
    # Training parameters
    'train_start': 10,    # Episodes before training starts
    'batch_size': 8,       # Replay memory batch size
    'mem_size': 50000,     # Replay memory size

    'discount': 0.95,       # Discount rate (gamma value)
    'lr': .0002,            # Learning reate

    # Model backups
    'load_file': 'saves/model-tank_737_1',
    'save_file': 'tank',
    'save_interval': 10,
    
    # Epsilon value (epsilon-greedy)
    'eps': 0.3155,             # Epsilon start value
    'eps_final': 0.1,       # Epsilon end value
    'eps_step': 10000       # Epsilon steps between start and end (linear)
}

dqn_engine = DQN(dqn_params)


def findDistance(start, end):
    return math.sqrt(math.pow(start[0] - end[0], 2) + math.pow(start[1] - end[1], 2))


class DQN_Tank(Tank):

    def __init__(self, x: int, y: int, textures=None, owner=constans.COMPUTER_TANK):
        super().__init__(x, y, textures, owner)
        self.numeps = 0
        self.total_steps_count = 0
        self.current_steps_count = 0

    def move(self):
        super().move()
        self.score += 1

    def initVariables(self):
        self.numeps += 1

        self.total_steps_count += self.current_steps_count
        self.current_steps_count = 0

        self.score = 0
        self.last_pos = (self.x, self.y)
        self.last_process = None
        self.total_reward = 0
        self.sess = tf.compat.v1.Session(
            config=tf.compat.v1.ConfigProto())
        self.dqn_engine = dqn_engine

        self.global_time = strftime(
            "%a_%d_%b_%Y_%H_%M_%S", localtime())

        self.Q_parameters = []
        self.cost_disp = 0
        self.params = dqn_params


        
        self.last_score = 0
        self.s = time()
        self.last_reward = 0.

        self.experiences = deque()
        self.last_scores = deque()

    def do_training(self):
        if (self.current_steps_count > self.params['train_start']):
            batch = random.sample(self.experiences, self.params['batch_size'])
            states_batch = []
            rewards_batch = []
            action_batch = []
            next_state_batch = []

            for i in batch:
                states_batch.append(i[0])
                rewards_batch.append(i[1])
                action_batch.append(i[2])
                next_state_batch.append(np.transpose(i[3]))
            states_batch = np.reshape(
                states_batch[0], (1, self.params['width'], self.params['height'], 1))
            rewards_batch = np.array(rewards_batch)
            action_batch = self.map_action_batch(np.array(action_batch))
            next_state_batch = np.reshape(
                next_state_batch[0], (1, self.params['width'], self.params['height'], 1))

            self.total_steps_count, self.cost_disp = self.dqn_engine.train(
                states_batch, action_batch, next_state_batch, rewards_batch)

    def map_action_batch(self, actions):
        new_actions = np.zeros((self.params['batch_size'], 4))
        for i in range(len(actions)):
            new_actions[i][int(
                list(self.move_sides.keys()).index(actions[i]))] = 1
        return new_actions

    def dqn_get_choice(self, game_map, enemies_coords):
        if self.x % (self.width / 2) == 0 and self.y % (self.width / 2) == 0:
            self.do_training_step(game_map, enemies_coords)
            if np.random.rand() > self.params['eps']:
                self.Q_prediction = self.dqn_engine.sess.run(
                    self.dqn_engine.y,
                    feed_dict={self.dqn_engine.x: np.reshape(game_map,
                                                             (1, self.params['width'], self.params['height'], 1)),
                               self.dqn_engine.q_t: np.zeros(1),
                               self.dqn_engine.actions: np.zeros((1, 4)),
                               self.dqn_engine.rewards: np.zeros(1)})[0]

                self.Q_parameters.append(max(self.Q_prediction))
                args_winner = np.argwhere(
                    self.Q_prediction == np.amax(self.Q_prediction))
                if len(args_winner) > 1:
                    new_side = list(self.move_sides.keys())[
                        args_winner[np.random.randint(0, len(args_winner))][0]]
                else:
                    new_side = list(self.move_sides.keys())[args_winner[0][0]]
            else:
                new_side = list(self.move_sides.keys())[
                    np.random.randint(0, 3)]

            self.current_side = new_side
            self.last_process = new_side
        elif self.x % (self.width / 2) == 0 or self.y % (self.width / 2) == 0:
            self.current_side = list(self.move_sides.keys())[
                random.randint(0, 3)]

    def do_training_step(self, game_map, enemies_coords, last_game_step=False):
        print("Step")
        if self.last_process is not None:
            self.last_state = np.copy(game_map)

            old_distances = list(map(lambda coord: findDistance(
                coord, self.last_pos), enemies_coords))
            mean_old_distance = sum(
                old_distances)/len(old_distances) if len(enemies_coords) != 0 else 0

            new_distances = list(map(lambda coord: findDistance(
                coord, (self.x, self.y)), enemies_coords))
            mean_new_distance = sum(
                new_distances)/len(new_distances) if len(enemies_coords) != 0 else 0

            # Process current experience reward
            self.current_score = self.score
            new_reward = self.current_score - self.last_score
            self.last_score = self.current_score

            if new_reward >= 280:
                self.last_reward = 200
            elif new_reward <= -80:
                self.last_reward = -700
            elif new_reward >= 1 :
                self.last_reward = 10

            self.last_reward += (mean_new_distance - mean_old_distance)*100

            self.total_reward += self.last_reward
            self.last_pos = (self.x, self.y)

            if last_game_step and dqn_params['save_file']:
                if self.current_steps_count > self.params['train_start']:
                    self.dqn_engine.save_ckpt(
                        'saves/model-' + dqn_params['save_file'] + "_" + str(self.total_steps_count) + '_' + str(self.numeps))

            experience = (self.last_state, float(self.last_reward),
                          self.last_process, game_map)
            self.experiences.append(experience)
            if len(self.experiences) > self.params['mem_size']:
                self.experiences.popleft()

            self.do_training()

        self.current_steps_count += 1
        self.params['eps'] = max(self.params['eps_final'],
                                 1.00 - float(self.total_steps_count) / float(self.params['eps_step']))
