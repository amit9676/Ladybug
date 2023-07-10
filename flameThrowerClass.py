import math

import pygame
from spriteHandler_Class import Sprite

'''flamethrower class, fired by ladybug and warwagon (and with the option of future units)'''
class Flamethrower:
    """main initlization of the flamethrower - takes the sprite, direction and x,y coordinates from external method.
    in addition initilize from vairables required for the object, such as radius, speed"""

    def __init__(self, game, caller, direction, emergence, logicSupport, radius=3, speed=5):
        self.__range = logicSupport.get_flamethrower_range()
        self.spr = Sprite(filename="flame001_5frames.png", frame_width=93, frame_height=self.__range,
                          num_rows=15, num_cols=5, frame_rate=23, num_rows_start=1)
        #self.spr = Sprite("flame002_original.png", 181, 404, 10, 5, 30, 0) #- bigger flamethrower for future use

        '''load initial parameters'''
        self.__image = self.spr.fill_frames_and_get_first_frame()
        self.__logicSupport = logicSupport
        self.__game = game
        self.__caller = caller

        '''the point of image in which the image will rotate around - in the flamethower image its the center
        of its width, and bottom of its height'''
        self.pivot = (self.spr.get_dimentions()[0]/2, self.spr.get_dimentions()[1])

        direction = self.__logicSupport.game_to_graph_axis_degrees(direction)
        self.radius = radius  # the distance from caller to pivot emergence point
        pos = self.__logicSupport.circular_emergernce_position(emergence, direction, self.radius)
        self.speed = speed

        self.original = self.__image
        self.current_time = pygame.time.get_ticks()
        self.__image, self.current_time = self.spr.update_animation_frame(self.current_time)
        self.__rect = self.original.get_rect()
        self.__mask = pygame.mask.from_surface(self.__image)

        self.__image, self.__rect = self.__logicSupport.blitRotate(self.original, pos, self.pivot, direction)
        self.self_destruct = False


    '''un used method, might be reused later'''
    def initilizeFlame(self, x, y):
        pass

    def get_rect(self) -> pygame.rect:
        return self.__rect

    def get_mask(self) -> pygame.rect:
        return self.__mask

    '''get flamethrower top range'''
    def get_range(self) -> int:
        return self.__range


    '''the method is responsible of updating the flamethrower - it gets from the outside the x and y coordinates of
    where to place the flamethrower, and a direction from which to extract the required angle for rotation'''

    def move(self, direction, emergence):
        direction = self.__logicSupport.game_to_graph_axis_degrees(direction)
        pos = self.__logicSupport.circular_emergernce_position(emergence, direction, self.radius)
        self.__image, self.__rect = self.__logicSupport.blitRotate(self.original, pos, self.pivot, direction)
        self.original, self.current_time = self.spr.update_animation_frame(self.current_time)
        self.__mask = pygame.mask.from_surface(self.__image)

        impacted = self.__logicSupport.impact_identifier(self, self.__caller, self.__game.get_ladybugs()
                                                         + self.__game.get_wagons())
        for i in impacted:
            i.decrease_hitPoints(1)
            i.flamethrower_hit()



    ''' draw the flame on screen'''
    def draw(self, surface):
        # Draw the image on the surface
        self.__logicSupport.draw(surface, self.__image, self.__rect)
