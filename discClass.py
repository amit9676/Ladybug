import math
import random
import time

import pygame
from InstanceClass import NPCInstance


class Disc:

    def __init__(self, window, mainActions, game, model, model_dimensions: (int, int) = (0, 0)):
        self.__game = game
        self.__mainActions = mainActions
        # self.__instance_struct = NPCInstance(team, mainActions)
        self.__image1 = pygame.image.load("disc_model.png")
        self.__image2 = pygame.image.load(f"{model}.png")
        self.__window = window

        '''Scale the images'''
        self.__image1 = pygame.transform.scale(self.__image1, (40, 40))
        downscale = self.__image2.get_height() / 30
        new_scale = (self.__image2.get_width() / downscale, self.__image2.get_height() / downscale)
        if model_dimensions != (0,0):
            new_scale = model_dimensions
        self.__image2 = pygame.transform.scale(self.__image2, new_scale)


        '''Store the images in a list'''
        self.__rect1 = self.__image1.get_rect()
        self.__rect2 = self.__image2.get_rect()
        # self.__pivots = ((30, 79), (17, 55), (15, 15))

        '''initlize mask'''
        self.__mask = pygame.mask.from_surface(self.__image1)

        # self.__location = (100,100)
        # self.__rect1.center = self.__location
        # self.__rect2.center = self.__rect1.center
        self.__initilizeDisc()
        self.__timer = pygame.time.get_ticks()
        self.__duration = random.randint(3, 15)
        self.self_destruct = False

        '''initlization on screen and destruction fields'''
        self.self_destruct = False  # public method

    '''this method is responsible for the creating itself of the wagon - where to place it (a bit outside the screen)
    and in which direction it will travel'''

    def __initilizeDisc(self):
        x = random.randint(20, self.__window[0] - self.__rect1.width / 2)
        y = random.randint(20, self.__window[1] - self.__rect1.height / 2)
        self.__rect1.center = (x, y)
        self.__rect2.center = self.__rect1.center
        return x, y

    def get_instance_struct(self):
        pass

    def get_rect(self):
        return self.__rect1

    def get_mask(self) -> pygame.rect:
        return self.__mask

    def get_current_location(self):
        return self.__rect.centerx, self.__rect.centery

    def update(self):
        impacted = self.__mainActions.impact_identifier(self, None, self.__game)
        if impacted:
            self.__game.create_warWagon(impacted[0].get_instance_struct().get_team())
            impacted = []
            self.self_destruct = True

        x = pygame.time.get_ticks() - self.__timer
        if x >= self.__duration * 1000:
            self.self_destruct = True

    def draw(self, surface):
        self.__mainActions.draw(surface, self.__image1, self.__rect1)
        self.__mainActions.draw(surface, self.__image2, self.__rect2)
        # pygame.draw.rect(surface, (255, 0, 0), self.__rect2, 2)
