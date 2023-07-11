# flag.py
import pygame
import random


# Define the Flag class
'''unused class as draft version of the game'''
class Flag:
    def __init__(self, window, mainActions):
        # Load the image
        self.__image = pygame.image.load("images/redFlag.png")
        self.__image = pygame.transform.scale(self.__image, (30, 30))
        self.__mainActions = mainActions
        self.__window = window

        # Get the rect of the image
        self.__rect = self.__image.get_rect()

        # Set the initial position to a random location on the screen
        self.__winMode = False
        self.initilize_instance()
        # self.__rect.x, self.__rect.y, self.__winMode =\
        #     self.mainActions.initilize_instance(self.get_rect().x, self.get_rect().y)

    def draw(self, surface):
        # Draw the image on the surface
        self.__mainActions.draw(surface, self.__image, self.__rect)

    def get_rect(self):
        return self.__rect

    def initilize_instance(self):
        self.__rect.x = random.randint(0, self.__window[0] - self.__rect.width)
        self.__rect.y = random.randint(0, self.__window[1] - self.__rect.height)
        self.winMode = False

    def win(self):
        self.__winMode = True
        self.__rect.x = -100
        self.__rect.y = -100
