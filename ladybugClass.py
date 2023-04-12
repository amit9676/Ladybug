# ladybug.py
import pygame
import random

from fireballClass import Fireball
from flameThrowerClass import Flamethrower
from InstanceClass import Instance


# Define the Ladybug class
from rocketClass import Rocket


class Ladybug:
    """initilize the ladybug with necessary parameters"""

    def __init__(self, window, mainActions, game, team):
        self._game = game
        self._team = team


        # Load the image
        self._image = pygame.image.load(f"ladybug_{team}.png")
        self._image = pygame.transform.scale(self._image, (30, 30))
        self._original = self._image
        self._window = window
        self._mainActions = mainActions

        # Get the rect of the image
        self._rect = self._image.get_rect()
        self._instance_struct: Instance = Instance(team, mainActions)

        self.fireballs = []
        self.flame = None
        self.rockets = []

        # Set the initial speed
        self._speed = 1.3
        self._winMode = False
        self.initilize_instance()

        '''direction variable for ladybug: 0 degrees is up; 90 -> right; 180 -> down; 270 -> left.
        each right/left pressing on arrow will change the degree in 5/-5 intervals.'''
        self._current_direction = 0

        '''the current_x and current_y are required for direction calculation with float number, the original
        rect.x and rect.y can only be integer, so for accurate path making at certain angle - floats are needed.
        hence the current_x and current_y'''
        self._current_x, self._current_y = self._mainActions.initilize_currents(self._rect.x, self._rect.y)

        self._last_shot_time = 0
        self._last_rocket_shot_time = 0

    def initilize_instance(self):
        self._rect.x = random.randint(0, self._window[0] - self._rect.width)
        self._rect.y = random.randint(0, self._window[1] - self._rect.height)
        self._winMode = False
        self._current_x, self._current_y = self._mainActions.initilize_currents(self._rect.x, self._rect.y)

    def get_rect(self) -> pygame.rect:
        return self._rect

    def get_current_location(self) -> (int, int):
        return self._rect.centerx, self._rect.centery

    def get_instance_struct(self) -> type(Instance):
        return self._instance_struct


    def _rotate_image(self):
        self._image = pygame.transform.rotate(self._original, -self._current_direction)
        center = self._rect.center
        self._rect = self._image.get_rect()
        self._rect.center = center
        return center

    def _boundary_keeping(self):
        if self._rect.left < 0:
            self._rect.left = 0
            self._current_x = 0
            self._rect.x = 0
        if self._rect.right > self._window[0]:
            self._rect.right = self._window[0]
            self._current_x = self._window[0] - self._image.get_width()
            self._rect.x = self._window[0] - self._image.get_width()
        if self._rect.top < 0:
            self._rect.top = 0
            self._current_y = 0
            self._rect.y = 0
        if self._rect.bottom > self._window[1]:
            self._rect.bottom = self._window[1]
            self._current_y = self._window[1] - self._image.get_height()
            self._rect.y = self._window[1] - self._image.get_height()

    '''the main ladybug method - check for any keyboard input and updates the ladybug according.
    the input includes movement and weapon using.'''

    def update(self):
        if self._winMode:
            return
        pass

    '''draw ladybug on screen'''

    def draw(self, surface):
        # Draw the image on the surface
        # surface.blit(self.image, self.rect)
        #pygame.draw.rect(surface, (140, 140, 21), self._rect, 2)
        self._mainActions.draw(surface, self._image, self._rect)
        #pygame.draw.circle(surface, (255, 25, 0), self._rect.center, 2, 0)


    '''if player wins - disable ladybug'''

    def win(self):
        self._winMode = True
        self._rect.x = -100
        self._rect.y = -100
        self.fireballs.clear()
        self.flame = None


    def manage_flamethrower(self):
        if self.flame is None:
            self.flame = Flamethrower(self._current_direction, self._rect.center,
                                      self._mainActions)
        else:
            self.flame.move(self._current_direction, self._rect.center)

    def add_rocket(self):
        self.rockets.append(Rocket(self._game, self._team,self._current_direction, self._rect.center,
                                   self._mainActions))
