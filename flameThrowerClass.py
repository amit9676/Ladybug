import math

import pygame
from spriteHandler_Class import Sprite


class Flamethrower:
    """main initlization of the flamethrower - takes the sprite, direction and x,y coordinates from external method.
    in addition initilize from vairables required for the object, such as radius, speed"""

    def __init__(self, direction, emergence_x, emergence_y, mainActions):
        self.spr = Sprite("flame001_5frames.png", 93, 216, 15, 5, 23, 1)
        #self.spr = Sprite("flame002_original.png", 181, 404, 10, 5, 30, 0)
        self.image = self.spr.fill_frames_and_get_first_frame()
        self.mainActions = mainActions

        self.pivot = (self.spr.get_dimentions()[0]/2, self.spr.get_dimentions()[1])
        direction = self.mainActions.game_to_graph_axis_degrees(direction)
        self.radius = 3
        pos = [emergence_x + math.cos(math.radians(direction)) * self.radius,
               emergence_y - math.sin(math.radians(direction)) * self.radius]
        self.speed = 5  # for now speed is hardcoded, if changes - the speed needs to be an input parameter.

        self.original = self.image
        self.current_time = pygame.time.get_ticks()
        self.image, self.current_time = self.spr.update_animation_frame(self.current_time)
        self.rect = self.original.get_rect()

        self.image, self.rect = self.mainActions.blitRotate(self.original,pos,self.pivot,direction-90)
        self.self_destruct = False


    '''un used method, might be reused later'''
    def initilizeFlame(self, x, y):
        pass


    '''the method is responsible of updating the flamethrower - it gets from the outside the x and y coordinates of
    where to place the flamethrower, and a direction from which to extract the required angle for rotation'''

    def move(self, direction, x, y):
        direction = self.mainActions.game_to_graph_axis_degrees(direction)
        pos = [x + math.cos(math.radians(direction)) * self.radius, y - math.sin(math.radians(direction)) * self.radius]
        self.image, self.rect = self.mainActions.blitRotate(self.original, pos, self.pivot, direction - 90)
        self.original, self.current_time = self.spr.update_animation_frame(self.current_time)


    ''' draw the flame on screen'''
    def draw(self, surface):
        # Draw the image on the surface
        self.mainActions.draw(surface,self.image,self.rect)
