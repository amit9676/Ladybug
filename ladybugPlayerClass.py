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

    def __init__(self, window, logicSupport, game, team):
        super().__init__(window, logicSupport, game, team)

    def update(self, keys):
        if self._winMode:
            return

        '''movement section'''
        # Move the ladybug based on the arrow key input
        '''turn left'''
        if keys[pygame.K_LEFT]:
            #self._current_direction = self.get_instance_struct().turn_left(self._current_direction)
            self._current_direction = self.get_instance_struct().turn(self._current_direction,-1)

        '''turn right'''
        if keys[pygame.K_RIGHT]:
            #self._current_direction = self.get_instance_struct().turn_right(self._current_direction)
            self._current_direction = self.get_instance_struct().turn(self._current_direction,1)

        '''advance'''
        if keys[pygame.K_UP]:
            self._current_x, self._current_y, self.get_rect().x, self.get_rect().y = self._logicSupport.advance(self._current_direction, self._speed, self._current_x, self._current_y)

        '''keep center point for smooth ladybug movment'''
        center = self._rotate_image()

        '''Keep the ladybug inside the window'''
        self._boundary_keeping()

        '''end of movement section'''

        '''weapons section'''
        '''fireball'''
        if keys[pygame.K_SPACE]:
            self.get_instance_struct().shoot(self._game, self, self._current_direction, center)
        self.get_instance_struct().update_fireballs(self)

        '''flamethrower'''
        if keys[pygame.K_a] and self._flamethrower > 0:
            self.manage_flamethrower()
        else:
            self.flame = None

        '''rocket'''
        if keys[pygame.K_s] and self._rockets > 0:
            self.get_instance_struct().launch_rocket(self, self._current_direction, center)
        self.get_instance_struct().update_rockets(self)
