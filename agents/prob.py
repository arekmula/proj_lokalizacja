# prob.py
# This is

import random
import numpy as np

from gridutil import *

best_turn = {('N', 'E'): 'turnright',
             ('N', 'S'): 'turnright',
             ('N', 'W'): 'turnleft',
             ('E', 'S'): 'turnright',
             ('E', 'W'): 'turnright',
             ('E', 'N'): 'turnleft',
             ('S', 'W'): 'turnright',
             ('S', 'N'): 'turnright',
             ('S', 'E'): 'turnleft',
             ('W', 'N'): 'turnright',
             ('W', 'E'): 'turnright',
             ('W', 'S'): 'turnleft'}


class LocAgent:

    def __init__(self, size, walls, eps_perc, eps_move):
        self.size = size
        self.walls = walls
        # list of valid locations
        self.locations = list({*locations(self.size)}.difference(self.walls))
        # dictionary from location to its index in the list
        self.loc_to_idx = {loc: idx for idx, loc in enumerate(self.locations)}
        self.eps_perc = eps_perc
        self.eps_move = eps_move

        # previous action
        self.prev_action = None

        # neighbours of each location (North, East, South, West)
        self.neighbours = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        # possible directions of robot
        self.directions = ['N', 'E', 'S', 'W']

        # starting direction of robot
        self.dir = None

        # Transition Factor for each location.
        self.T = np.zeros((len(self.locations), len(self.locations)), float)
        np.fill_diagonal(self.T, 1)  # fill diagonal with initial probabilty that robot is there

        # Sensor factor for each location. Each location contains four possible directions
        self.sensor = np.ones((len(self.locations), 4, 1), float)


        self.P = None

    def __call__(self, percept):
        # update posterior
        # TODO PUT YOUR CODE HERE

        self.updateSensorFactor(percept)


        # -----------------------

        action = 'forward'
        # TODO CHANGE THIS HEURISTICS TO SPEED UP CONVERGENCE
        # if there is a wall ahead then lets turn
        if 'fwd' in percept:
            # higher chance of turning left to avoid getting stuck in one location
            action = np.random.choice(['turnleft', 'turnright'], 1, p=[0.8, 0.2])
        else:
            # prefer moving forward to explore
            action = np.random.choice(['forward', 'turnleft', 'turnright'], 1, p=[0.8, 0.1, 0.1])

        self.prev_action = action

        return action


    def updateSensorFactor(self, percept):
        self.sensor[self.sensor>0] = 1
        # print(self.sensor)

        for loc_idx, loc in enumerate(self.locations):  # loop over each location

            if 'fwd' in percept:  # check if there was forward in percept

                for dir_idx, neigh in enumerate(self.neighbours):  # loop over each neighbour of current location
                    if (loc[0] + neigh[0], loc[1] + neigh[1]) not in self.locations:
                        self.sensor[loc_idx, dir_idx] = self.sensor[loc_idx, dir_idx] * 0.9
                    else:   # if there's no wall on North and wall wasn't detected by percept
                        self.sensor[loc_idx, dir_idx] = self.sensor[loc_idx, dir_idx] * 0.1

            if 'bckwd' in percept:  # check if there was backward in percept

                for dir_idx, neigh in enumerate(self.neighbours):  # loop over each neighbour of current location
                    if (loc[0] + neigh[0], loc[1] + neigh[1]) not in self.locations:
                        self.sensor[loc_idx, dir_idx] = self.sensor[loc_idx, dir_idx] * 0.9
                    else:   # if there's no wall on North and wall wasn't detected by percept
                        self.sensor[loc_idx, dir_idx] = self.sensor[loc_idx, dir_idx] * 0.1

            if 'left' in percept:  # check if there was left in percept

                for dir_idx, neigh in enumerate(self.neighbours):  # loop over each neighbour of current location
                    if (loc[0] + neigh[0], loc[1] + neigh[1]) not in self.locations:
                        self.sensor[loc_idx, dir_idx] = self.sensor[loc_idx, dir_idx] * 0.9
                    else:   # if there's no wall on North and wall wasn't detected by percept
                        self.sensor[loc_idx, dir_idx] = self.sensor[loc_idx, dir_idx] * 0.1



            if 'right' in percept:  # check if there was right in percept

                for dir_idx, neigh in enumerate(self.neighbours):  # loop over each neighbour of current location
                    if (loc[0] + neigh[0], loc[1] + neigh[1]) not in self.locations:
                        self.sensor[loc_idx, dir_idx] = self.sensor[loc_idx, dir_idx] * 0.9
                    else:   # if there's no wall on North and wall wasn't detected by percept
                        self.sensor[loc_idx, dir_idx] = self.sensor[loc_idx, dir_idx] * 0.1

        print(self.sensor)




    def getPosterior(self):
        # directions in order 'N', 'E', 'S', 'W'
        P_arr = np.zeros([self.size, self.size, 4], dtype=np.float)

        # put probabilities in the array
        # TODO PUT YOUR CODE HERE


        # -----------------------

        return P_arr

    def forward(self, cur_loc, cur_dir):
        if cur_dir == 'N':
            ret_loc = (cur_loc[0], cur_loc[1] + 1)
        elif cur_dir == 'E':
            ret_loc = (cur_loc[0] + 1, cur_loc[1])
        elif cur_dir == 'W':
            ret_loc = (cur_loc[0] - 1, cur_loc[1])
        elif cur_dir == 'S':
            ret_loc = (cur_loc[0], cur_loc[1] - 1)
        ret_loc = (min(max(ret_loc[0], 0), self.size - 1), min(max(ret_loc[1], 0), self.size - 1))
        return ret_loc, cur_dir

    def backward(self, cur_loc, cur_dir):
        if cur_dir == 'N':
            ret_loc = (cur_loc[0], cur_loc[1] - 1)
        elif cur_dir == 'E':
            ret_loc = (cur_loc[0] - 1, cur_loc[1])
        elif cur_dir == 'W':
            ret_loc = (cur_loc[0] + 1, cur_loc[1])
        elif cur_dir == 'S':
            ret_loc = (cur_loc[0], cur_loc[1] + 1)
        ret_loc = (min(max(ret_loc[0], 0), self.size - 1), min(max(ret_loc[1], 0), self.size - 1))
        return ret_loc, cur_dir

    @staticmethod
    def turnright(cur_loc, cur_dir):
        dir_to_idx = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        dirs = ['N', 'E', 'S', 'W']
        idx = (dir_to_idx[cur_dir] + 1) % 4
        return cur_loc, dirs[idx]

    @staticmethod
    def turnleft(cur_loc, cur_dir):
        dir_to_idx = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
        dirs = ['N', 'E', 'S', 'W']
        idx = (dir_to_idx[cur_dir] + 4 - 1) % 4
        return cur_loc, dirs[idx]
