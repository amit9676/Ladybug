import math

import pygame
from spriteHandler_Class import Sprite


class Explosion:
    """this class plays eploxsion which occurs on impact of missile in any unit,
     or when time for its runtime runs out"""

    def __init__(self, mainActions, position):
        # self.spr = Sprite("explosion.png", 142, 200, 4, 5, 35, 0)
        self.spr = Sprite("explosion_medium.png", 56, 80, 4, 5, 35, 0)
        #self.spr = Sprite("explosion_small.png", 28, 40, 4, 5, 35, 0)
        self.__image = self.spr.fill_frames_and_get_first_frame()
        self.mainActions = mainActions


        self.original = self.__image
        self.current_time = pygame.time.get_ticks()
        self.__image, self.current_time = self.spr.update_animation_frame(self.current_time)
        self.__rect = self.original.get_rect()
        self.__rect.centerx ,self.__rect.centery = position

        self.self_destruct = False
        self.__counter = 0

    def move(self):
        if self.__counter == 19:
            self.self_destruct = True
        img = self.__image
        self.__image, self.current_time = self.spr.update_animation_frame(self.current_time)



        if img != self.__image:
            self.__counter+=1


    def get_image(self):
        return self.__image

    def get_rect(self):
            return self.__rect

    ''' draw the flame on screen'''
    def draw(self, surface):
        # Draw the image on the surface
        self.mainActions.draw(surface,self.__image,self.rect)
        #pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)
