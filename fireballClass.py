import math

import pygame
import main
from main import WINDOW_WIDTH, WINDOW_HEIGHT

class Fireball:
    def __init__(self, direction, emergence_x, emergence_y):
        self.image = pygame.image.load("fireball.png")
        self.image = pygame.transform.scale(self.image, (6, 6))
        self.speed = 10

        # Get the rect of the image
        self.rect = self.image.get_rect()

        self.emergence_x = emergence_x
        self.emergence_y = emergence_y
        self.direction = direction
        self.initilizeBullet()
        self.current_x = float(self.rect.x)
        self.current_y = float(self.rect.y)
        self.self_destruct = False
        self.winMode = False


    def initilizeBullet(self):
        self.rect.x = self.emergence_x
        self.rect.y = self.emergence_y
        self.current_x = float(self.rect.x)
        self.current_y = float(self.rect.y)
        self.winMode = False

    '''move fireball at the pre determined path'''
    def move(self):
        self.current_x, self.current_y, self.rect.x, self.rect.y = \
            main.trigo(self.direction, self.speed, self.current_x, self.current_y)

        #
        if self.rect.left < 0 or self.rect.right > WINDOW_WIDTH or self.rect.top < 0 or self.rect.bottom > WINDOW_HEIGHT:
            self.self_destruct = True

    def draw(self, surface):
        # Draw the image on the surface
        surface.blit(self.image, self.rect)
