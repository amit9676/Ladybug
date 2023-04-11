# ladybug.py
import math

import pygame
import random

from fireballClass import Fireball
from ladybugClass import Ladybug
from flameThrowerClass import Flamethrower
from InstanceClass import NPCInstance


# Define the Ladybug class
class Ladybug_NPC(Ladybug):
    """initilize the ladybug with necessary parameters"""

    def __init__(self, window, mainActions, game, team):
        super().__init__(window, mainActions, game, team)

        '''which inctance this inctance is targeting at any moment'''
        self._instance_struct = NPCInstance(team, mainActions)
        self.__target = None
        self.__desired_direction = self.get_instance_struct().get_desired_direction(self.__target, self.get_rect())
        #print(f"a: {self.__desired_direction}")


    def make_turn(self):
        current_dir = self._current_direction
        desired_dir = self.__desired_direction

        # If the current and desired direction are the same, return None
        if current_dir == desired_dir:
            return 0

        # Calculate the difference between the current and desired direction
        diff = desired_dir - current_dir

        # If the difference is greater than 180, turn the opposite direction
        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360

        # If the difference is positive, turn right; otherwise, turn left
        if diff > 0:
            #self.__current_direction = (self.__current_direction + 1) % 360
            self.turn_right()
        else:
            self.turn_left()
        return diff


    '''the main ladybug method - check for any keyboard input and updates the ladybug according.
    the input includes movement and weapon using.'''

    def update(self):
        if super().update():
            return

        #return
        self.__target = self.get_instance_struct().get_target(self._game)
        self.__desired_direction = self.get_instance_struct().get_desired_direction(self.__target, self.get_rect())
        diff = self.make_turn()

        dist = self.get_instance_struct().calculate_distance(self.__target, self.get_rect())
        center = self._rotate_image()

        #print(diff)
        # if dist <= 100:
        #     self.manage_flamethrower()
        # else:
        #     self.flame = None
        # if diff <= abs(100):
        #     self.advance()
        #print(diff)
        if diff == 0:
            self.get_instance_struct().shoot(self, self._current_direction, center)
        self.get_instance_struct().update_fireballs(self)

