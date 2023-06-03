# ladybug.py
import math

import pygame
import random

from fireballClass import Fireball
from ladybugClass import Ladybug
from flameThrowerClass import Flamethrower
from InstanceClass import NPCInstance


# Define the Ladybug class
'''npc ladybug class - inherent from ladybug class and contains actions and fields which are for computer controlled
lady bug'''
class Ladybug_NPC(Ladybug):
    """initilize the ladybug with necessary parameters"""

    def __init__(self, window, mainActions, game, team):
        super().__init__(window, mainActions, game, team)

        '''which inctance this inctance is targeting at any moment'''
        self._instance_struct: NPCInstance = NPCInstance(team, mainActions)
        self.__target = None
        self.__desired_direction = self.get_instance_struct().get_desired_direction(self.__target, self.get_rect())
        #print(f"a: {self.__desired_direction}")



    '''the main ladybug method - check for any keyboard input and updates the ladybug according.
    the input includes movement and weapon using.'''

    def update(self):
        if super().update():
            return

        self.__target = self.get_instance_struct().get_target(self._game)
        self.__desired_direction = self.get_instance_struct().get_desired_direction(self.__target, self.get_rect())
        self._current_direction,diff = self.get_instance_struct().make_turn(self._current_direction,self.__desired_direction)

        dist = self.get_instance_struct().calculate_distance(self.__target, self.get_rect())
        center = self._rotate_image()

        #print(diff)
        # if dist <= 100:
        #     self.manage_flamethrower()
        # else:
        #     self.flame = None
        if dist >= abs(100):
            self._current_x, self._current_y, self.get_rect().x, self.get_rect().y = self._mainActions.advance(self._current_direction, self._speed, self._current_x, self._current_y)
        #print(diff)

        if self._rockets > 0:
            self.get_instance_struct().launch_rocket(self, self._current_direction, center)

        else:
            if diff == 0:
                self.get_instance_struct().shoot(self._game, self, self._current_direction, center)
        self.get_instance_struct().update_rockets(self)
        self.get_instance_struct().update_fireballs(self)

