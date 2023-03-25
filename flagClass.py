# flag.py
import pygame
import random
from main import WINDOW_WIDTH, WINDOW_HEIGHT

# Define the Flag class
class Flag:
    def __init__(self):
        # Load the image
        self.image = pygame.image.load("redFlag.png")
        self.image = pygame.transform.scale(self.image, (30, 30))

        # Get the rect of the image
        self.rect = self.image.get_rect()

        # Set the initial position to a random location on the screen
        self.winMode = False
        self.initilizeGame()

    def draw(self, surface):
        # Draw the image on the surface
        surface.blit(self.image, self.rect)


    def initilizeGame(self):
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, WINDOW_HEIGHT - self.rect.height)
        self.winMode = False

    def win(self):
        self.winMode = True
        self.rect.x = -100
        self.rect.y = -100
