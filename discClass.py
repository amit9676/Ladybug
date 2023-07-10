import math
import random
import time

import pygame
from InstanceClass import NPCInstance


class Disc:
    """The Disc Class is a disc represent either a weapon or a unit..

    currently there are 3 kinds of Discs:
    a. warwagon - the unit that activates the disk summons war wagon to target enemy unit.
    b. rocket ammunition - activating the rocket disc will give the activating unit a random number of rocket
    in range of 3-10. note: the ammunition will be given only if the activating unit can fire rockets, else the disc
    activating will be disregarded.
    c. flamethrower ammunition - same with rockets but with flamethrower, giving 500 to 1500 flames.

    this class is an abstract class and has 2 child classes:
    a. DiscGame - used by the game - full information at the DiscGame class.
    b. DiscDisplay - used to display current ammunition to the player.
    """
    def __init__(self, logicSupport, model, model_dimensions: (int, int) = (0, 0)):
        self._logicSupport = logicSupport
        # self.__instance_struct = NPCInstance(team, mainActions)
        self._image1 = pygame.image.load("disc_model.png")
        self._image2 = pygame.image.load(f"{model}.png")
        '''Scale the images'''
        '''default scaling: scale the model to approximate 30 pixels'''
        self._image1 = pygame.transform.scale(self._image1, (40, 40))
        self._downScale(30,model_dimensions)

        '''Store the images in a list'''
        self._rect1 = self._image1.get_rect()
        #self._rect2 = self._image2.get_rect()
        self._model = model

    '''scale the image object properly into disc dimensions'''
    def _downScale(self, scale, model_dimensions):
        downscale = self._image2.get_height() / scale
        new_scale = (self._image2.get_width() / downscale, self._image2.get_height() / downscale)

        '''there is also an option to enter custom scale for input'''
        if model_dimensions != (0, 0):
            new_scale = model_dimensions
        self._image2 = pygame.transform.scale(self._image2, new_scale)
        self._rect2 = self._image2.get_rect()

    '''get disc dimensions'''
    def get_dimensions(self) -> (int,int):
        return self._rect1.width, self._rect1.height

    def get_model(self) -> str:
        return self._model

    def get_type(self):
        return "disc"

    def draw(self, surface):
        self._logicSupport.draw(surface, self._image1, self._rect1)
        self._logicSupport.draw(surface, self._image2, self._rect2)
        #pygame.draw.rect(surface, (30, 125, 162), self._rect1,2)
