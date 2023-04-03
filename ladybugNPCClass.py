# ladybug.py
import math

import pygame
import random

from fireballClass import Fireball
from flameThrowerClass import Flamethrower


# Define the Ladybug class
class Ladybug_NPC:
    """initilize the ladybug with necessary parameters"""

    def __init__(self, window, mainActions, game, team):
        self.game = game
        self.__team = team

        # Load the image
        self.__image = pygame.image.load(f"ladybug_{team}.png")
        self.__image = pygame.transform.scale(self.__image, (30, 30))
        self.__original = self.__image
        self.__window = window
        self.__mainActions = mainActions

        # Get the rect of the image
        self.__rect = self.__image.get_rect()

        self.fireballs = []
        self.flame = None

        # Set the initial speed
        self.__speed = 1.3
        self.__winMode = False
        self.initilize_instance()

        '''direction variable for ladybug: 0 degrees is up; 90 -> right; 180 -> down; 270 -> left.
        each right/left pressing on arrow will change the degree in 5/-5 intervals.'''
        self.__current_direction = 0

        '''the current_x and current_y are required for direction calculation with float number, the original
        rect.x and rect.y can only be integer, so for accurate path making at certain angle - floats are needed.
        hence the current_x and current_y'''
        self.__current_x, self.__current_y = self.__mainActions.initilize_currents(self.__rect.x, self.__rect.y)

        self.__last_shot_time = 0

        '''which inctance this inctance is targeting at any moment'''
        self.__target = None
        self.__desired_direction = self.__get_desired_direction()

    def initilize_instance(self):
        self.__rect.x = random.randint(0, self.__window[0] - self.__rect.width)
        self.__rect.y = random.randint(0, self.__window[1] - self.__rect.height)
        self.__winMode = False
        self.__current_x, self.__current_y = self.__mainActions.initilize_currents(self.__rect.x, self.__rect.y)

    def get_rect(self):
        return self.__rect

    def get_team(self):
        return self.__team


    '''this method is responsible for the NPC to acquire a target to attack'''
    def __get_target(self):
        for ins in self.game.inctances:
            if ins.get_team() != self.__team:
                self.__target = ins

    def __get_desired_direction(self):
        if self.__target is None:
            return
        dx = self.__rect.centerx - self.__target.get_current_location()[0]
        dy = self.__rect.centery - self.__target.get_current_location()[1]
        angle = math.atan2(dy, dx)
        direction = math.degrees(angle) % 360
        direction = int(direction)
        direction = (direction - 90) % 360
        #print(direction)
        return direction
        #self.__desired_direction = int(direction)
        #self.__desired_direction = (self.__desired_direction - 90) % 360
        #print(self.__desired_direction)



    def make_turn(self):
        current_dir = self.__current_direction
        desired_dir = self.__desired_direction

        # If the current and desired direction are the same, return None
        if current_dir == desired_dir:
            return None

        # Calculate the difference between the current and desired direction
        diff = desired_dir - current_dir

        # If the difference is greater than 180, turn the opposite direction
        if diff > 180:
            diff -= 360
        elif diff < -180:
            diff += 360

        # If the difference is positive, turn right; otherwise, turn left
        if diff > 0:
            #self.__current_direction = (self.__current_direction + 1) % 360
            self.turn_right()
            return "right"
        else:
            self.turn_left()
            return "left"


    def get_current_location(self):
        return self.__rect.centerx, self.__rect.centery

    def turn_right(self):
        self.__current_direction = (self.__current_direction + 1) % 360

    def turn_left(self):
        self.__current_direction = (self.__current_direction - 1) % 360

    def advance(self):
        self.__current_x, self.__current_y, self.__rect.x, self.__rect.y = \
            self.__mainActions.trigo(self.__current_direction, self.__speed, self.__current_x, self.__current_y)

    def __rotate_image(self):
        self.__image = pygame.transform.rotate(self.__original, -self.__current_direction)
        center = self.__rect.center
        self.__rect = self.__image.get_rect()
        self.__rect.center = center

    '''the main ladybug method - check for any keyboard input and updates the ladybug according.
    the input includes movement and weapon using.'''

    def update(self):
        if self.__winMode:
            return

        self.__get_target()
        self.__desired_direction = self.__get_desired_direction()
        self.make_turn()
        self.__rotate_image()
        #print(f"d: {self.__desired_direction}")

        # distance_to_turn = abs(self.__current_direction - self.__desired_direction)
        # print(f"distance to turn {distance_to_turn}")
        # if 180 >= distance_to_turn > 0:
        #     self.turn_right()
        # elif distance_to_turn > 180:
        #     self.turn_left()



        # '''keep center point for smooth ladybug movment'''
        # self.__image = pygame.transform.rotate(self.__original, -self.__current_direction)
        # center = self.__rect.center
        # self.__rect = self.__image.get_rect()
        # self.__rect.center = center
        #
        # '''Keep the ladybug inside the window'''
        # if self.__rect.left < 0:
        #     self.__rect.left = 0
        #     self.__current_x = 0
        #     self.__rect.x = 0
        # if self.__rect.right > self.__window[0]:
        #     self.__rect.right = self.__window[0]
        #     self.__current_x = self.__window[0] - self.__image.get_width()
        #     self.__rect.x = self.__window[0] - self.__image.get_width()
        # if self.__rect.top < 0:
        #     self.__rect.top = 0
        #     self.__current_y = 0
        #     self.__rect.y = 0
        # if self.__rect.bottom > self.__window[1]:
        #     self.__rect.bottom = self.__window[1]
        #     self.__current_y = self.__window[1] - self.__image.get_height()
        #     self.__rect.y = self.__window[1] - self.__image.get_height()
        #
        # '''end of movement section'''
        #
        # '''weapons section'''
        # '''fireball'''
        # if keys[pygame.K_SPACE]:
        #     self.__shoot(self.__current_direction, center[0],
        #                  center[1])
        # for fireball in self.fireballs:
        #     fireball.move()  # update fireball
        #     if fireball.self_destruct:
        #         '''for every game update we check if fireball has crossed the boundries,
        #         if so - the fireball is destroyed and removed from list and game memory.'''
        #         self.fireballs.remove(fireball)
        #
        # '''flamethrower'''
        # if keys[pygame.K_a]:
        #     if self.flame is None:
        #         self.flame = Flamethrower(self.__current_direction, self.__rect.center[0], self.__rect.center[1],
        #                                   self.__mainActions)
        #     else:
        #         self.flame.move(self.__current_direction, self.__rect.center[0], self.__rect.center[1])
        #
        # else:
        #     self.flame = None

    '''draw ladybug on screen'''

    def draw(self, surface):
        # Draw the image on the surface
        # surface.blit(self.image, self.rect)
        self.__mainActions.draw(surface, self.__image, self.__rect)

    '''if player wins - disable ladybug'''

    def win(self):
        self.__winMode = True
        self.__rect.x = -100
        self.__rect.y = -100
        self.fireballs.clear()
        self.flame = None

    '''fireball shoot method'''

    def __shoot(self, direction, x, y):
        current_time = pygame.time.get_ticks()

        if current_time - self.__last_shot_time >= 333:
            self.__last_shot_time = current_time
            self.fireballs.append(Fireball(direction, x, y, self.__mainActions))
            '''add new fireball instance to the fireball list'''
