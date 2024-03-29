import math
import random
from discClass import Disc

import pygame
from InstanceClass import NPCInstance


class DiscGame(Disc):
    """The Disc Class is a disc which a moving (ground) unit can take for some assistance.
    it appears to a random amount of short time in random location, and if activated by a unit when reaching it
     - it provides the required assistance.

    this is a child class of Disc, and its main purpose to be picked up by ladybugs for bonuses."""
    def __init__(self, window, logicSupport, game, model, model_dimensions: (int, int) = (0, 0)):
        self.__game = game
        super().__init__(logicSupport, model, model_dimensions)

        self.__window = window


        '''initlize mask'''
        self.__mask = pygame.mask.from_surface(self._image1)

        self.__initilizeDisc()
        self.__timer = pygame.time.get_ticks()
        self.__duration = random.randint(1, 8)
        self.self_destruct = False

    '''this method is responsible for the creating the disc at random point in the window'''

    def __initilizeDisc(self):
        x = random.randint(20, self.__window[0] - self._rect1.width / 2)
        y = random.randint(20, self.__window[1] - self._rect1.height / 2)
        self._rect1.center = (x, y)
        self._rect2.center = self._rect1.center
        return x, y

    def get_rect(self):
        return self._rect1

    def get_mask(self) -> pygame.rect:
        return self.__mask

    def get_current_location(self):
        return self._rect1.centerx, self._rect1.centery


    '''update the disc - check for any activations and disable when the lifetime of it exceeded.'''
    def update(self):
        x = pygame.time.get_ticks() - self.__timer
        if x >= self.__duration * 1000:
            self.self_destruct = True

