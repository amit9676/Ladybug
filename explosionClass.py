import math

import pygame
from spriteHandler_Class import Sprite


class Explosion:
    """this class plays explosion which occurs on impact of missile in any unit,
     or when time for its runtime runs out"""

    def __init__(self, logicSupport, position):
        # self.spr = Sprite("explosion.png", 142, 200, 4, 5, 35, 0)
        self.spr = Sprite(filename="images/explosion_medium.png", frame_width=56, frame_height=80,
                          num_rows=4, num_cols=5, frame_rate=35, num_rows_start=0)
        # self.spr = Sprite("explosion_small.png", 28, 40, 4, 5, 35, 0)
        self.__image = self.spr.fill_frames_and_get_first_frame()
        self.__logicSupport = logicSupport

        self.original = self.__image
        self.current_time = pygame.time.get_ticks()
        self.__image, self.current_time = self.spr.update_animation_frame(self.current_time)
        self.__rect = self.original.get_rect()
        self.__rect.centerx, self.__rect.centery = position

        self.self_destruct = False
        self.__counter = 0

    '''play the animation, according to set framerate'''
    def move(self):
        '''this condition is needed to make sure the animation plays once only, and then dissappears.'''
        if self.__counter == 19:
            self.self_destruct = True
        img = self.__image
        self.__image, self.current_time = self.spr.update_animation_frame(self.current_time)

        '''this condition is needed to make sure the counter wont increase too fast, but as accordingly to framerate'''
        if img != self.__image:
            self.__counter += 1

    def get_image(self):
        return self.__image

    def get_rect(self):
        return self.__rect

    ''' draw the flame on screen'''

    def draw(self, surface):
        # Draw the image on the surface
        self.__logicSupport.draw(surface, self.__image, self.__rect)
        # pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)
