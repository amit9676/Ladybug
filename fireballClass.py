import math

import pygame


class Fireball:
    def __init__(self, game, caller, direction, emergence, mainActions, speed=2):
        self.__game = game
        self.__caller = caller

        self.__image = pygame.image.load("fireball.png")
        self.__image = pygame.transform.scale(self.__image, (6, 6))
        self.__mainActions = mainActions
        self.__speed = speed

        # Get the rect of the image
        self.__rect = self.__image.get_rect()
        self.__mask = pygame.mask.from_surface(self.__image)

        self.__emergence_x, self.__emergence_y = emergence
        self.__direction = direction
        self.__initilizeBullet()
        self.__current_x, self.__current_y = self.__mainActions.initilize_currents(self.__rect.x, self.__rect.y)
        self.self_destruct = False
        self.__winMode = False

    def get_rect(self) -> pygame.rect:
        return self.__rect

    def get_mask(self) -> pygame.rect:
        return self.__mask

    def __initilizeBullet(self):
        self.__rect.centerx = self.__emergence_x
        self.__rect.centery = self.__emergence_y
        #self.__current_x, self.__current_y = self.__mainActions.initilize_currents(self.__rect.x, self.__rect.y)
        self.__winMode = False

    '''move fireball at the pre determined path'''

    def move(self):
        self.__current_x, self.__current_y, self.__rect.x, self.__rect.y = \
            self.__mainActions.advance(self.__direction, self.__speed, self.__current_x, self.__current_y)

        impacted = self.__mainActions.impact_identifier(self, self.__caller, self.__game)
        if impacted:
            self.self_destruct = True
            impacted[0].decrease_hitPoints(10)
            #print(impacted[0].get_hitpoints())

        if self.__mainActions.check_for_boundary_crossing(self.__rect, self.__game.get_window_size()):
            self.self_destruct = True

    def draw(self, surface):
        # Draw the image on the surface
        self.__mainActions.draw(surface, self.__image, self.__rect)
        #pygame.draw.rect(surface, (140, 140, 21), self.__rect, 2)
