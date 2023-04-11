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
            self.turn_left()

        '''turn right'''
        if keys[pygame.K_RIGHT]:
            self.turn_right()

        '''advance'''
        if keys[pygame.K_UP]:
            self.advance()

        '''keep center point for smooth ladybug movment'''
        center = self._rotate_image()
        #print(f"center: {center}\n")

        '''Keep the ladybug inside the window'''
        self._boundry_keeping()

        '''end of movement section'''

        '''weapons section'''
        '''fireball'''
        if keys[pygame.K_SPACE]:
            self.get_instance_struct().shoot(self, self._current_direction, center[0],
                                     center[1])
        self.get_instance_struct().update_fireballs(self)

        '''flamethrower'''
        if keys[pygame.K_a]:
            self.manage_flamethrower()

        else:
            self.flame = None
