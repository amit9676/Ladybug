# ladybug.py
import pygame
import random

from ladybugClass import Ladybug
from fireballClass import Fireball
from flameThrowerClass import Flamethrower


# Define the Ladybug class
class Ladybug_Player(Ladybug):
    """initilize the ladybug with necessary parameters"""

    def __init__(self, window, mainActions, game, team):
        super().__init__(window, mainActions, game, team)

    def update(self, keys):
        if self._winMode:
            return

        '''movement section'''
        # Move the ladybug based on the arrow key input
        '''turn left'''
        if keys[pygame.K_LEFT]:
            self._current_direction = self.get_instance_struct().turn_left(self._current_direction)

        '''turn right'''
        if keys[pygame.K_RIGHT]:
            self._current_direction = self.get_instance_struct().turn_right(self._current_direction)

        '''advance'''
        if keys[pygame.K_UP]:
            self._current_x, self._current_y, self.get_rect().x, self.get_rect().y = self._mainActions.advance(self._current_direction, self._speed, self._current_x, self._current_y)

        '''keep center point for smooth ladybug movment'''
        center = self._rotate_image()

        '''Keep the ladybug inside the window'''
        self._boundary_keeping()

        '''end of movement section'''

        '''weapons section'''
        '''fireball'''
        if keys[pygame.K_SPACE]:
            self.get_instance_struct().shoot(self, self._current_direction, center)
        self.get_instance_struct().update_fireballs(self)

        '''flamethrower'''
        if keys[pygame.K_a]:
            self.manage_flamethrower()

        else:
            self.flame = None
