"""
GridWorld

Simple game - copied and adapted from

https://github.com/awjuliani/DeepRL-Agents/blob/master/gridworld.py
"""
from abc import ABC, abstractmethod
import copy

from m2mlearning.games.Base import BaseGame


import numpy as np
import random
import itertools
import scipy.misc
import matplotlib.pyplot as plt


class GridWorldObject(ABC):
    """Class representing an in-game object"""
    def __init__(self):
        self.__coordinates = None

    def get_coordinates(self):
        return self.__coordinates

    def set_coordinates(self, coords):
        self.__coordinates = coords

    def clear_coordinates(self):
        self.__coordinates = None

    @abstractmethod
    def get_channel(self):
        pass

    @abstractmethod
    def get_reward(self):
        """Returns the reward.

        It returns an integer (positive, 0 or negative)
        for the amount of reward.
        It returns None if the game should end.
        """
        pass
    
class GridWorldHero(GridWorldObject):
    """The Hero"""

    def __init__(self):
        pass

    def get_channel(self):
        return 2

    def get_reward(self):
        return 0, False


class GridWorldFire(GridWorldObject):
    """A Fire(place)"""

    def __init__(self, deadly=False):
        self.__deadly = deadly

    def get_channel(self):
        return 0

    def get_reward(self):
        return 0, self.__deadly


class GridWorldTreasure(GridWorldObject):
    """A Treasure"""

    def __init__(self):
        pass

    def get_channel(self):
        return 1

    def get_reward(self):
        return 1, False

        
class GridWorld(BaseGame):
    """GridWorld Game

    This is a small grid world game where a hero collecting treasures
    and avoiding fires.

    Each collected treasure give a +1 reward.

    There are two different versions of the game available:
    When the hero reaches a fire 
    1 - the game ends
    2 - a reward of -1 is given.

    Also there is the possiblity to specify the size of the
    gameboard and how many treasures and fires are placed
    on the gameboard.
    """

    def __init__(self, fire_is_deadly=True, penalty_for_oob=True,
                 board_size = [7, 7], treasures=4, fires=2):
        self.__board_size = board_size
        # Need three colors - many information is coded into colors
        self.__view_size = copy.deepcopy(self.__board_size)
        self.__view_size.append(3)
        self.__treasure_cnt = treasures
        self.__fire_cnt = fires
        # Is there a penalty for out-off-board movements?
        self.__penalty_for_oob = penalty_for_oob
        self.__penalty = -0.001
        # Be sure to be able to place all the elements and have some
        # spare places. (The one is added because of the hero.)
        assert self.__board_size[0] * self.__board_size[1] // 2 \
            > self.__treasure_cnt + self.__fire_cnt + 1 

        # Indexed via self.__objects
        self.__game_board = np.ndarray(self.__board_size, dtype=np.int8)

        # Index 0 is the None object
        # Index 1 is the Hero
        self.__objects = [None, GridWorldHero()]
        for _ in range(self.__treasure_cnt):
            self.__objects.append(GridWorldTreasure())
        for _ in range(self.__fire_cnt):
            self.__objects.append(GridWorldFire(fire_is_deadly))

        self.__movements = np.array([
            [  0,  1], # 0: up
            [  0, -1], # 1: down
            [ -1,  0], # 2: left
            [  1,  0], # 3: right
        ])

    def __get_free_position(self):
        """Returns an empty board position

        The algorithm here can be optimized!
        Currently only random fields are chosen and dropped if
        they are already allocated.
        """
        while True:
            x = random.randrange(0, self.__board_size[0])
            y = random.randrange(0, self.__board_size[1])
            if self.__game_board[x, y] == 0:
                return (x, y)

    def __render(self):
        """Renders the board and returns an 'picture' of the size 84x84x3"""
        image = np.zeros(self.__view_size)
        for x in range(0, self.__board_size[0]):
            for y in range(0, self.__board_size[1]):
                if self.__game_board[x, y] == 0:
                    continue
                image[x, y, self.__objects[self.__game_board[x, y]].get_channel() ] = 1
                
        img_r = scipy.misc.imresize(image[:,:,0], [84,84,1], interp='nearest')
        img_g = scipy.misc.imresize(image[:,:,1], [84,84,1], interp='nearest')
        img_b = scipy.misc.imresize(image[:,:,2], [84,84,1], interp='nearest')
        return np.stack([img_r, img_g, img_b],axis=2)

    def action_space_size(self):
        return len(self.__movements)
        
    def reset(self):
        """Resets the game

        Clears the internal object storage and places the objects
        (treasure, fire, hero) on random points.
        """
        # 0 is the None object
        self.__game_board.fill(0)

        for obj_idx in range(1, len(self.__objects)):
            free_position = self.__get_free_position()
            self.__game_board[free_position] = obj_idx
            self.__objects[obj_idx].set_coordinates(free_position)

        return self.__render()

    def __new_hero_coordinates(self, direction):
        # 0 - up, 1 - down, 2 - left, 3 - right

        new_hero_coordinates \
            = self.__objects[1].get_coordinates() + self.__movements[direction]

        def check_coordinates(axis):
            if new_hero_coordinates[axis] < 0:
                new_hero_coordinates[axis] = 0
                return self.__penalty
        
            if new_hero_coordinates[axis] >= self.__board_size[axis]:
                new_hero_coordinates[axis] = self.__board_size[axis] - 1
                return self.__penalty

            return 0.0

        penalty = check_coordinates(0)
        penalty += check_coordinates(1)

        return new_hero_coordinates, penalty
    
    def __collision_detection(self, new_hero_coordinates):
        move_object_idx = self.__game_board[new_hero_coordinates[0], new_hero_coordinates[1]]
        cur_hero_coordinates = self.__objects[1].get_coordinates()

        if cur_hero_coordinates[0] == new_hero_coordinates[0] \
           and cur_hero_coordinates[1] == new_hero_coordinates[1]:
            return 0.0, False

        if move_object_idx != 0:
            reward, done = self.__objects[move_object_idx].get_reward()
            if done:
                return reward, True
            
            self.__game_board[cur_hero_coordinates[0], cur_hero_coordinates[1]] = 0
            self.__game_board[new_hero_coordinates[0], new_hero_coordinates[1]] = 1 # Hero
            self.__objects[1].set_coordinates(new_hero_coordinates)
            fp = self.__get_free_position()
            self.__game_board[fp[0], fp[1]] = move_object_idx
            self.__objects[move_object_idx].set_coordinates(fp)
            return reward, False
        else:
            # Just set the coordinates of the hero and empty the current field
            self.__game_board[cur_hero_coordinates[0], cur_hero_coordinates[1]] = 0
            self.__game_board[new_hero_coordinates[0], new_hero_coordinates[1]] = 1 # Hero
            self.__objects[1].set_coordinates(new_hero_coordinates)
            return 0.0, False

    def step(self, action):
        new_hero_coordinates, penalty = self.__new_hero_coordinates(action)
        reward, done = self.__collision_detection(new_hero_coordinates)
        return self.__render(), (reward+penalty), done, None
