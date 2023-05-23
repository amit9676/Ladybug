import math

import pygame
from spriteHandler_Class import Sprite


class Flamethrower:
    """main initlization of the flamethrower - takes the sprite, direction and x,y coordinates from external method.
    in addition initilize from vairables required for the object, such as radius, speed"""

    def __init__(self,game,caller, direction, emergence, mainActions, radius=3, speed=5):
        self.spr = Sprite("flame001_5frames.png", 93, 216, 15, 5, 23, 1)
        #self.spr = Sprite("flame002_original.png", 181, 404, 10, 5, 30, 0)
        self.__image = self.spr.fill_frames_and_get_first_frame()
        self.__mainActions = mainActions
        self.__game = game
        self.__caller = caller

        self.pivot = (self.spr.get_dimentions()[0]/2, self.spr.get_dimentions()[1])
        direction = self.__mainActions.game_to_graph_axis_degrees(direction)
        self.radius = radius
        pos = self.__mainActions.circular_emergernce_position(emergence,direction,self.radius)
        self.speed = speed

        self.original = self.__image
        self.current_time = pygame.time.get_ticks()
        self.__image, self.current_time = self.spr.update_animation_frame(self.current_time)
        self.__rect = self.original.get_rect()
        self.__mask = pygame.mask.from_surface(self.__image)

        self.__image, self.__rect = self.__mainActions.blitRotate(self.original,pos,self.pivot,direction)
        self.self_destruct = False


    '''un used method, might be reused later'''
    def initilizeFlame(self, x, y):
        pass

    def get_rect(self) -> pygame.rect:
        return self.__rect

    def get_mask(self) -> pygame.rect:
        return self.__mask


    '''the method is responsible of updating the flamethrower - it gets from the outside the x and y coordinates of
    where to place the flamethrower, and a direction from which to extract the required angle for rotation'''

    def move(self, direction, emergence):
        direction = self.__mainActions.game_to_graph_axis_degrees(direction)
        pos = self.__mainActions.circular_emergernce_position(emergence,direction,self.radius)
        self.__image, self.__rect = self.__mainActions.blitRotate(self.original, pos, self.pivot, direction )
        self.original, self.current_time = self.spr.update_animation_frame(self.current_time)
        self.__mask = pygame.mask.from_surface(self.__image)

        impacted = self.__mainActions.impact_identifier(self, self.__caller, self.__game)
        for i in impacted:
            i.decrease_hitPoints(1)



    ''' draw the flame on screen'''
    def draw(self, surface):
        # Draw the image on the surface
        self.__mainActions.draw(surface,self.__image,self.__rect)
