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
    def __init__(self, window, mainActions, game, model, model_dimensions: (int, int) = (0, 0)):
        self.__game = game
        super().__init__(mainActions, model, model_dimensions)

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
        impacted = self._mainActions.impact_identifier(self, None, self.__game)
        if impacted:
            if self._model == "warWagon_model":
                self.__game.create_warWagon(impacted[0].get_instance_struct().get_team())
            elif self._model == "rocket":
                '''the try catch is needed in case some unit (war wagon or any future unit that wont shoot rockets)
                attempts to pickup the rocket disc (which they can with collision) - that they dont have the method
                "add_rockets" - the game wont crash.
                so only when unit that able to fire rockets (lady bug or potential future unit that fires rockets)
                the rockets will be added.'''
                try:
                    impacted[0].add_rockets()
                except:
                    pass
            elif self._model == "flame001_model":
                try:
                    impacted[0].add_flamethrower()
                except:
                    pass

            impacted = []
            self.self_destruct = True

        x = pygame.time.get_ticks() - self.__timer
        if x >= self.__duration * 1000:
            self.self_destruct = True

