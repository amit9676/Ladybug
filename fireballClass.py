import math

import pygame


class Fireball:
    def __init__(self, direction, emergence_x, emergence_y, mainActions):
        self.__image = pygame.image.load("fireball.png")
        self.__image = pygame.transform.scale(self.__image, (6, 6))
        self.__mainActions = mainActions
        self.__speed = 10

        # Get the rect of the image
        self.__rect = self.__image.get_rect()

        self.__emergence_x = emergence_x
        self.__emergence_y = emergence_y
        self.__direction = direction
        self.__initilizeBullet()
        self.__current_x, self.__current_y = self.__mainActions.initilize_currents(self.__rect.x, self.__rect.y)
        self.self_destruct = False
        self.__winMode = False

    def __initilizeBullet(self):
        self.__rect.x = self.__emergence_x
        self.__rect.y = self.__emergence_y
        self.__current_x, self.__current_y = self.__mainActions.initilize_currents(self.__rect.x, self.__rect.y)
        self.__winMode = False

    '''move fireball at the pre determined path'''

    def move(self):
        window_size = self.__mainActions.get_window()
        self.__current_x, self.__current_y, self.__rect.x, self.__rect.y = \
            self.__mainActions.trigo(self.__direction, self.__speed, self.__current_x, self.__current_y)

        #
        # if self.__rect.left < 0 or self.__rect.right > window_size[0] or self.__rect.top < 0 \
        #         or self.__rect.bottom > window_size[1]:
        #     self.self_destruct = True
        if self.__mainActions.check_for_boundry_crossing(self.__rect):
            self.self_destruct = True

    def draw(self, surface):
        # Draw the image on the surface
        self.__mainActions.draw(surface, self.__image, self.__rect)
