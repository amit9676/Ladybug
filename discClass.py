import math
import random
import time

import pygame
from InstanceClass import NPCInstance


class Disc:

    def __init__(self, window, mainActions, game, model):
        '''wagon initlization'''
        self.__game = game
        self.__mainActions = mainActions
        #self.__instance_struct = NPCInstance(team, mainActions)
        self.__image1 = pygame.image.load("disc_model.png")
        self.__image2 = pygame.image.load(f"{model}.png")
        self.__window = window


        '''Scale the images'''
        self.__image1 = pygame.transform.scale(self.__image1, (40, 40))
        downscale = self.__image2.get_height() / 30
        self.__image2 = pygame.transform.scale(self.__image2, (self.__image2.get_width() / downscale, self.__image2.get_height() / downscale))

        '''Store the images in a list'''
        self.__rect1 = self.__image1.get_rect()
        self.__rect2 = self.__image2.get_rect()
        #self.__pivots = ((30, 79), (17, 55), (15, 15))

        '''initlize mask'''
        self.__mask = pygame.mask.from_surface(self.__image1)

        self.__location = (100,100)
        self.__rect1.center = self.__location
        self.__rect2.center = self.__rect1.center





        '''initlization on screen and destruction fields'''
        self.self_destruct = False  # public method

    '''this method is responsible for the creating itself of the wagon - where to place it (a bit outside the screen)
    and in which direction it will travel'''

    def initilizeDisc(self):
        pass



    def get_instance_struct(self):
        pass

    def get_rect(self):
        return self.__rect

    def get_mask(self) -> pygame.rect:
        return self.__mask

    def get_current_location(self):
        return self.__rect.centerx, self.__rect.centery

    '''update wagon movement - the wagon will always move straight. no turns - when it will finishes crossing the
    screen - it will be considered as non active and will be self destrcuted.'''

    def update(self):
        pass

    def draw(self, surface):
        self.__mainActions.draw(surface, self.__image1, self.__rect1)
        self.__mainActions.draw(surface, self.__image2, self.__rect2)
        #pygame.draw.rect(surface, (255, 0, 0), self.__rect2, 2)

