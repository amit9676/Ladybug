# ladybug.py
import pygame
import random

import main
from fireballClass import Fireball
from flameThrowerClass import Flamethrower
from main import WINDOW_WIDTH, WINDOW_HEIGHT
import math

# Define the Ladybug class
class Ladybug:
    """initilize the ladybug with necessary parameters"""
    def __init__(self):
        # Load the image
        self.image = pygame.image.load("ladybug.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.original = self.image

        # Get the rect of the image
        self.rect = self.image.get_rect()

        self.fireballs = []
        self.flame = None

        # Set the initial speed
        self.speed = 5
        self.winMode = False
        self.initilizeGame()

        '''direction variable for ladybug: 0 degrees is up; 90 -> right; 180 -> down; 270 -> left.
        each right/left pressing on arrow will change the degree in 5/-5 intervals.'''
        self.current_direction = 0

        '''the current_x and current_y are required for direction calculation with float number, the original
        rect.x and rect.y can only be integer, so for accurate path making at certain angle - floats are needed.
        hence the current_x and current_y'''
        self.current_x = float(self.rect.x)
        self.current_y = float(self.rect.y)

        self.last_shot_time = 0



    '''lady bug initilization method on screen - the ladybug is placed randomly on screen.'''
    def initilizeGame(self):
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, WINDOW_HEIGHT - self.rect.height)
        self.current_x = float(self.rect.x)
        self.current_y = float(self.rect.y)
        self.winMode = False


    '''the main ladybug method - check for any keyboard input and updates the ladybug according.
    the input includes movement and weapon using.'''
    def update(self, keys):
        if self.winMode:
            return

        '''movement section'''
        # Move the ladybug based on the arrow key input
        '''turn left'''
        if keys[pygame.K_LEFT]:
            self.current_direction = (self.current_direction - 5) % 360

        '''turn right'''
        if keys[pygame.K_RIGHT]:
            self.current_direction = (self.current_direction + 5) % 360

        '''advance'''
        if keys[pygame.K_UP]:
            self.current_x, self.current_y, self.rect.x, self.rect.y =\
                main.trigo(self.current_direction, self.speed, self.current_x, self.current_y)

        '''keep center point for smooth ladybug movment'''
        self.image = pygame.transform.rotate(self.original, -self.current_direction)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

        '''Keep the ladybug inside the window'''
        if self.rect.left < 0:
            self.rect.left = 0
            self.current_x = 0
            self.rect.x = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.current_x = WINDOW_WIDTH - self.image.get_width()
            self.rect.x = WINDOW_WIDTH - self.image.get_width()
        if self.rect.top < 0:
            self.rect.top = 0
            self.current_y = 0
            self.rect.y = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.current_y = WINDOW_HEIGHT - self.image.get_height()
            self.rect.y = WINDOW_HEIGHT - self.image.get_height()

        '''end of movement section'''


        '''weapons section'''

        '''fireball'''
        if keys[pygame.K_SPACE]:
            self.__shoot(self.current_direction,center[0],
                       center[1])
        for fireball in self.fireballs:
            fireball.move() # update fireball
            if fireball.self_destruct:
                '''for every game update we check if fireball has crossed the boundries,
                if so - the fireball is destroyed and removed from list and game memory.'''
                self.fireballs.remove(fireball)

        '''flamethrower'''
        if keys[pygame.K_a]:
            if self.flame is None:
                self.flame = Flamethrower(self.current_direction, self.rect.center[0], self.rect.center[1])
            else:
                self.flame.move(self.current_direction, self.rect.center[0], self.rect.center[1])

        else:
            self.flame = None




    '''draw ladybug on screen'''
    def draw(self, surface):
        # Draw the image on the surface
        surface.blit(self.image, self.rect)

    '''if player wins - disable ladybug'''
    def win(self):
        self.winMode = True
        self.rect.x = -100
        self.rect.y = -100
        self.fireballs.clear()
        self.flame = None

    '''fireball shoot method'''
    def __shoot(self, direction, x, y):
        current_time = pygame.time.get_ticks()

        if current_time - self.last_shot_time >= 333:
            self.last_shot_time = current_time
            self.fireballs.append(Fireball(direction,x,y))
            '''add new fireball instance to the fireball list'''


