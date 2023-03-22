import pygame
from main import WINDOW_WIDTH, WINDOW_HEIGHT

class Fireball:
    def __init__(self, direction, emergence_x, emergence_y,extra_x, extra_y):
        self.image = pygame.image.load("fireball.png")
        self.image = pygame.transform.scale(self.image, (5, 5))
        self.speed = 10

        # Get the rect of the image
        self.rect = self.image.get_rect()

        self.emergence_x = emergence_x + extra_x
        self.emergence_y = emergence_y + extra_y
        self.direction = direction
        self.initilizeBullet()
        self.self_destruct = False
        self.winMode = False


    def initilizeBullet(self):
        self.rect.x = self.emergence_x

        self.rect.y = self.emergence_y
        self.winMode = False

    def move(self):

        if self.direction == 0:
            self.rect.y -= self.speed
        elif self.direction == 45:
            self.rect.y -= self.speed
            self.rect.x -= self.speed
        elif self.direction == 90:
            self.rect.x -= self.speed
        elif self.direction == 135:
            self.rect.y += self.speed
            self.rect.x -= self.speed
        elif self.direction == 180:
            self.rect.y += self.speed
        elif self.direction == 225:
            self.rect.y += self.speed
            self.rect.x += self.speed
        elif self.direction == 270:
            self.rect.x += self.speed
        elif self.direction == 315:
            self.rect.y -= self.speed
            self.rect.x += self.speed

        #
        if self.rect.left < 0 or self.rect.right > WINDOW_WIDTH or self.rect.top < 0 or self.rect.bottom > WINDOW_HEIGHT:
            self.self_destruct = True

    def draw(self, surface):
        # Draw the image on the surface
        surface.blit(self.image, self.rect)
