# ladybug.py
import pygame
import random

from ladybugClass import Ladybug
from fireballClass import Fireball
from flameThrowerClass import Flamethrower

# Define the Ladybug
'''player ladybug class - inherent from ladybug class and contains actions and fields which are for player controlled
lady bug'''


class Ladybug_Player(Ladybug):
    """initilize the ladybug with necessary parameters"""

    def __init__(self, window, logicSupport, game, team, keys):
        super().__init__(window, logicSupport, game, team)
        self.__keys = self.__get_pygame_key(keys)

    def __get_pygame_key(self, codes):
        pygame_keys = [None] * len(codes)
        for attr_name in dir(pygame):

            if attr_name.startswith('K_'):
                attr_value = getattr(pygame, attr_name)
                if isinstance(attr_value, int) and attr_value in codes:
                    index = codes.index(attr_value)
                    pygame_keys[index] = attr_value
        return pygame_keys

    def update(self, keys):
        if self._winMode:
            return

        '''movement section'''
        # Move the ladybug based on the arrow key input
        '''turn left'''
        if keys[self.__keys[2]]:
            # self._current_direction = self.get_instance_struct().turn_left(self._current_direction)
            self._current_direction = self.get_instance_struct().turn(self._current_direction, -1)

        '''turn right'''
        if keys[self.__keys[1]]:
            # self._current_direction = self.get_instance_struct().turn_right(self._current_direction)
            self._current_direction = self.get_instance_struct().turn(self._current_direction, 1)

        '''advance'''
        if keys[self.__keys[0]]:
            self._current_x, self._current_y, self.get_rect().x, self.get_rect().y = self._logicSupport.advance(
                self._current_direction, self._speed, self._current_x, self._current_y)
            self._current_speed = self._speed
        else:
            self._current_speed = 0

        '''keep center point for smooth ladybug movment'''
        center = self._rotate_image()

        '''updating velocity'''
        vel = self._logicSupport.calculate_velocity(self._current_speed,
                                                    self._logicSupport.game_to_graph_axis_degrees(self._current_direction))
        self._velocity[0], self._velocity[1] = vel[0], vel[1]


        '''Keep the ladybug inside the window'''
        self._boundary_keeping()
        '''end of movement section'''

        '''weapons section'''
        '''fireball'''
        if keys[self.__keys[3]]:
            self.get_instance_struct().shoot(self._game, self, self._current_direction, center)
        self.get_instance_struct().update_fireballs(self)

        '''flamethrower'''
        if keys[self.__keys[4]] and self._flamethrower > 0:
            self.manage_flamethrower()
        else:
            self.flame = None

        '''rocket'''
        if keys[self.__keys[5]] and self._rockets > 0:
            self.get_instance_struct().launch_rocket(self, self._current_direction, center)
        self.get_instance_struct().update_rockets(self)
