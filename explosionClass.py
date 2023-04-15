import math

import pygame
from spriteHandler_Class import Sprite


class Explosion:
    """this class plays eploxsion which occurs on impact of missile in any unit,
     or when time for its runtime runs out"""

    def __init__(self, mainActions, position):
        self.spr = Sprite("explosion.png", 142, 200, 4, 5, 25, 0)
        self.image = self.spr.fill_frames_and_get_first_frame()
        self.mainActions = mainActions


        #self.pivot = (self.spr.get_dimentions()[0]/2, self.spr.get_dimentions()[1])
        #direction = self.mainActions.game_to_graph_axis_degrees(direction)
        #self.radius = radius
        #pos = self.mainActions.circular_emergernce_position(emergence,direction,self.radius)
        #self.speed = speed

        self.original = self.image
        self.current_time = pygame.time.get_ticks()
        self.image, self.current_time = self.spr.update_animation_frame(self.current_time)
        self.rect = self.original.get_rect()
        self.rect.x ,self.rect.y = position

        #self.image, self.rect = self.mainActions.blitRotate(self.original,pos,self.pivot,direction)
        self.self_destruct = False
        self.__counter = 0

    def move(self):
        #direction = self.mainActions.game_to_graph_axis_degrees(direction)
        #pos = self.mainActions.circular_emergernce_position(emergence,direction,self.radius)
        #self.image, self.rect = self.mainActions.blitRotate(self.original, pos, self.pivot, direction )
        if self.__counter == 20:
            self.self_destruct = True
        self.image, self.current_time = self.spr.update_animation_frame(self.current_time)

        self.__counter+=1
        #print("?")


    ''' draw the flame on screen'''
    def draw(self, surface):
        # Draw the image on the surface
        self.mainActions.draw(surface,self.image,self.rect)
        #pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)
