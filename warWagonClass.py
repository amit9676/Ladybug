import math
import random
import time

import pygame
from InstanceClass import NPCInstance

class WarWagon:
    """main initialization of the war wagon - the object of this class is comprised of 3 parts - the wagon, the machine
    gun and  operator lady bug, in the initialization method we initialize the images.
    the war wagon should operate the following: it is being initialized in some following spot OUTSIDE the screen,
    close to it - and with a direction, such that traveling in the direction will make it enter the screen.
    the wagon will travel in the direction in straight line (no turns) until it crosses the screen.
    in the active time (the time the wagon is visible on screen - the machine gun mounted on it will fire at any enemies
    it will locate."""

    def __init__(self, window, mainActions, game, team):
        self.__game = game
        self.__mainActions = mainActions
        self.__image1 = pygame.image.load("wagon.png")
        self.__image2 = pygame.image.load("machine_gun.png")
        self.__image3 = pygame.image.load(f"ladybug_{team}.png")
        self.__window = window

        # Scale the images
        self.__image1 = pygame.transform.scale(self.__image1, (60, 108))
        self.__image2 = pygame.transform.scale(self.__image2, (35, 70))
        self.__image3 = pygame.transform.scale(self.__image3, (30, 30))

        # Store the images in a list
        self.__images = [self.__image1, self.__image2, self.__image3]
        self.__originals = [self.__image1, self.__image2, self.__image3]
        self.__rects = [self.__image1.get_rect(), self.__image2.get_rect(), self.__image3.get_rect()]
        self.__pivots = ((30, 79), (17, 55), (15, 15))
        self.__current_direction = 0
        self.__rotate_direction = 0
        self.__rotate_direction2 = 0
        self.__current_x, self.__current_y = self.initilizeWagon()
        self.__speed = 0.25

        self.__instance_struct = NPCInstance(team, mainActions)
        self.__target = None
        self.__desired_direction = self.get_instance_struct().get_desired_direction(self.__target, self.get_rect())

        self.self_destruct = False  # public method
        self.__active = False

    '''this method is resposible for the creating itself of the wagon - where to place it (a bit outside the screen)
    and in which direction it will travel'''

    def initilizeWagon(self):
        #self.__rects[1].center = -100, -100
        self.__rects[2].center = -100, -100

        direction = self.__generate_random_direction()
        self.__current_direction = direction
        rotate_direction = self.__mainActions.game_to_graph_axis_degrees(direction) - 90
        self.__rotate_direction = rotate_direction
        self.__rotate_direction2 = self.__rotate_direction


        x, y = self.__initilizePlacement(self.__current_direction)
        print(f"x: {x}, y: {y}, dir: {self.__current_direction}")

        for i in range(1,len(self.__images)):
            self.__images[i], self.__rects[i] = self.__mainActions.blitRotate(self.__images[i], (x, y),
                                                                              self.__pivots[i], rotate_direction)

        #time.sleep(0.5)
        return x, y

    '''rectangle section - in here we are taking care of all rectangle related methods which are necessary to handle
    the random placement of the cart.
    all the rectangle functions work with the following input:
    ((top-left), (top-right), (bottom-right), (bottom-left)) that each of them is (x,y) tuple and represents a rectangle
    corner. the functions will work ONLY on rectangles which sides are parallel to x,y axis.'''

    '''this method get the direction in which the cart will travel - and calculate a possible random location for
     the cart initialization such that: a. the location will be outside the screen.
      b: the cart will immediately travel toward the screen at straight line.
      
      input: one or 2 rectangles in which the wagon should be places.
      output: a point randomly selected from the rectangles, there we weill place the wagon'''
    def __initilizePlacement(self, direction):
        #print(direction)

        # rectangle tuple = (top-left,top-right,bottom-right,bottom-left)
        # for diagonal angles - rect_a = hotizonal, rect_b = vertical
        cart_width, cart_height = self.__images[0].get_height(), self.__images[0].get_height()

        if direction == 0:
            rect_a = ((cart_width, self.__window[1]),
                      (self.__window[0] - cart_width, self.__window[1]),
                      (self.__window[0] - cart_width, self.__window[1] + cart_height),
                      (cart_width, self.__window[1] + cart_height))
            return self.__random_point_within_rect(rect_a)
        elif direction == 45:
            rect_a = ((-cart_width, self.__window[1]),
                      (self.__window[0] - cart_width, self.__window[1]),
                      (self.__window[0], self.__window[1] + cart_height),
                      (-cart_width, self.__window[1] + cart_height))
            rect_b = ((-cart_width, cart_height),
                      (0, cart_height),
                      (0, self.__window[1] + cart_height),
                     (-cart_width, self.__window[1] + cart_height))
            return self.__random_point_within_union(rect_a, rect_b)
        elif direction == 90:
            rect_a = ((-cart_width, cart_height),
                      (0, cart_height),
                      (0, self.__window[1] - cart_height),
                      (-cart_width, self.__window[1] - cart_height))
            return self.__random_point_within_rect(rect_a)
        elif direction == 135:
            rect_a = ((-cart_width, -cart_height),
                      (self.__window[0] - cart_width, -cart_height),
                      (self.__window[0] - cart_width, 0),
                      (-cart_width, 0))
            rect_b = ((-cart_width, -cart_height),
                      (0, -cart_height),
                      (0, self.__window[1] - cart_height),
                      (-cart_width, self.__window[1] - cart_height))
            return self.__random_point_within_union(rect_a, rect_b)
        elif direction == 180:
            rect_a = ((cart_width, -cart_height),
                      (self.__window[0] - cart_width, -cart_height),
                      (self.__window[0] - cart_width, 0),
                      (cart_width, 0))
            return self.__random_point_within_rect(rect_a)
        elif direction == 225:
            rect_a = ((cart_width, -cart_height),
                      (self.__window[0] + cart_width, -cart_height),
                      (self.__window[0] + cart_width, 0),
                      (cart_width, 0))
            rect_b = ((self.__window[0], -cart_height),
                      (self.__window[0] + cart_width, -cart_height),
                      (self.__window[0] + cart_width, self.__window[1] - cart_height),
                      (self.__window[0], self.__window[1] - cart_height))
            return self.__random_point_within_union(rect_a, rect_b)
        elif direction == 270:
            rect_a = ((self.__window[0], cart_height),
                      (self.__window[0] + cart_width, cart_height),
                      (self.__window[0] + cart_width, self.__window[1] - cart_height),
                      (self.__window[0], self.__window[1] - cart_height))
            return self.__random_point_within_rect(rect_a)
        elif direction == 315:
            rect_a = ((cart_width, self.__window[1]),
                      (self.__window[0] + cart_width, self.__window[1]),
                      (self.__window[0] + cart_width, self.__window[1] + cart_height),
                      (cart_width, self.__window[1] + cart_height))
            rect_b = ((self.__window[0], cart_height),
                      (self.__window[0] + cart_width, cart_height),
                      (self.__window[0] + cart_width, self.__window[1] + cart_height),
                      (self.__window[0], self.__window[1] + cart_height))
            return self.__random_point_within_union(rect_a, rect_b)
        return None  # function should NOT get here, if it does - the input is invalid


    '''calculate a random direction in which the cart will travel - the possible directions are up, down, right, left
    and diagonals it means the possible values are 0, 45, 90, 135, 180, 225, 270, 315'''
    def __generate_random_direction(self):
        return random.randint(0, 7) * 45


    '''aid method to return a random point within the broundries of a rectangle, NOT including the edges'''
    def __random_point_within_rect(self, rect):

        x = random.randint(rect[0][0] + 1, rect[1][0] - 1)
        y = random.randint(rect[0][1] + 1, rect[3][1] - 1)
        return x, y


    '''aid method to return a random point within one of two input rectangles.
    because there is an intersection between the 2 rectangles - the chance the random point will be in the
    intersection is higher than outside of it.'''
    def __random_point_within_union(self, rect_a, rect_b):
        rect = random.choice((rect_a, rect_b))
        return self.__random_point_within_rect(rect)

    '''end of rectangle section'''


    def get_instance_struct(self):
        return self.__instance_struct

    def get_rect(self):
        return self.__rects[0]

    def get_current_location(self):
        return self.__rects[0].centerx, self.__rects[0].centery

    '''update wagon movement - the wagon will always move straight. no turns - when it will finishes crossing the
    screen - it will be considered as non active and will be self destrcuted.'''
    def update(self):

        self.__current_x, self.__current_y, a, b = \
            self.__mainActions.trigo(self.__current_direction, self.__speed, self.__current_x, self.__current_y)

        self.__images[0], self.__rects[0] = self.__mainActions.blitRotate(self.__originals[0], (a, b),
                                                                          self.__pivots[0], self.__rotate_direction)

        self.__images[1], self.__rects[1] = self.__mainActions.blitRotate(self.__originals[1], (a, b),
                                                                          self.__pivots[1], self.__rotate_direction2)

        self.__images[2], self.__rects[2] = self.__mainActions.blitRotate(self.__originals[2], (a, b),
                                                                          self.__pivots[2], self.__rotate_direction2)

        #self.rotate_direction2 += 1
        #self.rotate_direction2 %= 360
        if self.__target is None:
            self.__target = self.get_instance_struct().get_target(self.__game)
        self.__desired_direction = self.get_instance_struct().get_desired_direction(self.__target, self.get_rect())
        print(f"cd: {self.__current_direction}, rd2: {self.__rotate_direction2},"
              f" rd2: {self.__mainActions.game_to_graph_axis_degrees(self.__rotate_direction2) - 90}")
        self.__rotate_direction2 = self.__mainActions.game_to_graph_axis_degrees(self.__rotate_direction2) - 90
        self.__rotate_direction2, diff = self.get_instance_struct().\
            make_turn(self.__rotate_direction2, self.__desired_direction)

        if diff == 0:
            self.get_instance_struct().shoot\
                (self.__rotate_direction2, self.__rects[1].centerx,self.__rects[1].centery, 4, 100)
        self.get_instance_struct().update_fireballs()
        self.__rotate_direction2 = self.__mainActions.game_to_graph_axis_degrees(self.__rotate_direction2) - 90

        '''# self.rotate_direction2, diff = self.get_instance_struct().\
        #     make_turn(self.rotate_direction2, self.__desired_direction)
        self.rotate_direction2 = self.__desired_direction
        print(f"desired direction: {self.__desired_direction}, rotate direction2: {self.rotate_direction2}")'''

        '''shooting section'''
        # self.__target = self.get_instance_struct().get_target(self.__game)
        # self.__desired_direction = self.get_instance_struct().get_desired_direction(self.__target, self.get_rect())
        #
        #
        #
        # dist = self.get_instance_struct().calculate_distance(self.__target, self.get_rect())
        #
        #
        # if diff == 0:
        #     self._shoot(self.__current_direction, center[0], center[1])
        # self._update_fireballs()


        if not self.__active:
            self.__active = not self.__mainActions.check_for_boundry_crossing(self.__rects[0])
        else:
            self.self_destruct = self.__mainActions.check_for_boundry_crossing(self.__rects[0])

    def draw(self, surface):

        for img, rect in zip(self.__images, self.__rects):
            surface.blit(img, rect)

        #pygame.draw.rect(surface, (255, 0, 0), self.__rects[0], 2)
        #pygame.draw.rect(surface, (140, 140, 21), self.__rects[1], 2)
        #pygame.draw.circle(surface, (0, 255, 0), (250, 250), 7, 0)
        # pygame.draw.circle(surface, (195, 145, 145),  (self.rects[0].centerx,self.rects[0].centery + 25), 7, 0)
