import math
import random

import pygame


class WagonGun:
    """main initlization of the flamethrower - takes the sprite, direction and x,y coordinates from external method.
    in addition initilize from vairables required for the object, such as radius, speed"""

    def __init__(self, window, mainActions):
        self.mainActions = mainActions
        self.image1 = pygame.image.load("wagon.png")
        self.image2 = pygame.image.load("machine_gun.png")
        self.image3 = pygame.image.load("ladybug_blue.png")
        self.__window = window

        # Scale the images
        self.image1 = pygame.transform.scale(self.image1, (60, 108))
        self.image2 = pygame.transform.scale(self.image2, (35, 70))
        self.image3 = pygame.transform.scale(self.image3, (30, 30))

        # Store the images in a list
        self.images = [self.image1, self.image2, self.image3]
        self.originals = [self.image1, self.image2, self.image3]
        self.rects = [self.image1.get_rect(), self.image2.get_rect(), self.image3.get_rect()]
        self.initilizeWagon(250, 250)

    '''un used method, might be reused later'''

    def initilizeWagon(self, x1, y1):
        # print(f"{self.rects[0].center}, {self.rects[0].centerx}, {self.rects[0].centery}")
        # print(f"{self.rects[0].x}, {self.rects[0].y}")
        # print()
        # self.rects[0].center = (x, y-25)
        self.rects[1].center = -100, -100
        self.rects[2].center = -100, -100
        # print(f"{self.rects[0].center}, {self.rects[0].centerx}, {self.rects[0].centery}")
        # print(f"{self.rects[0].x}, {self.rects[0].y}")
        direction = self.__generate_random_direction()
        direction = self.mainActions.game_to_graph_axis_degrees(direction) - 90
        x, y = self.__initilizePlacement(direction)
        self.images[0], self.rects[0] = self.mainActions.blitRotate(self.originals[0], (x, y), (30, 79), direction)

    def __initilizePlacement(self, direction):
        # outerSquare tuple = (top-left,top-right,bottom-right,bottom-left)
        # for diagonal angles - rect_a = hotizonal, rect_b = vertical
        cart_width, cart_height = self.images[1].get_height(), self.images[0].get_height()
        outerSquare = ((-cart_width, -cart_height),
                       (self.__window[0] + cart_width, -cart_height),
                       (self.__window[0] + cart_width, self.__window[1] + cart_height),
                       (-cart_width, self.__window[1] + cart_height))
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
                      outerSquare[3])
            rect_b = ((-cart_width, cart_height),
                      (0, cart_height),
                      (0, self.__window[1] + cart_height),
                      outerSquare[3])
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
                      (self.__window[0] + cart_width, self.__window[1] + cart_height),
                      (self.__window[0] + cart_width, self.__window[1] + cart_height),
                      (self.__window[0], cart_height))
            return self.__random_point_within_union(rect_a, rect_b)
        return None  # function should NOT get here, if it does - the input is invalid

    def __generate_random_direction(self):
        return random.randrange(0, 7) * 45

    def __random_point_within_rect(self, rect):

        x = random.randint(rect[0][0] + 1, rect[1][0] - 1)
        y = random.randint(rect[0][1] + 1, rect[3][1] - 1)
        return (x, y)

    def __random_point_within_union(self, rect_a, rect_b):
        # Compute the bounding box of the union of the two rectangles
        left = min(rect_a[0][0], rect_a[3][0], rect_b[0][0], rect_b[3][0])
        right = max(rect_a[1][0], rect_a[2][0], rect_b[1][0], rect_b[2][0])
        top = min(rect_a[0][1], rect_a[1][1], rect_b[0][1], rect_b[1][1])
        bottom = max(rect_a[2][1], rect_a[3][1], rect_b[2][1], rect_b[3][1])

        # Generate random points within the bounding box until one falls within the union
        while True:
            x = random.randint(left, right)
            y = random.randint(top, bottom)
            if self.__is_point_within_rect((x, y), rect_a) or self.__is_point_within_rect((x, y), rect_b):
                return (x, y)

    def __is_point_within_rect(self, point, rect):
        # Check if a point is within a rectangle
        x, y = point
        x_min = rect[0][0] + 1
        x_max = rect[2][0] - 1
        y_min = rect[0][1] + 1
        y_max = rect[2][1] - 1
        return x_min < x < x_max and y_min < y <= y_max

    def update(self):
        for img in self.images:
            img.get_rect()

    def draw(self, surface):

        for img, rect in zip(self.images, self.rects):
            surface.blit(img, rect)

        pygame.draw.rect(surface, (255, 0, 0), self.rects[0], 2)
        pygame.draw.circle(surface, (0, 255, 0), (250, 250), 7, 0)
        # pygame.draw.circle(surface, (195, 145, 145),  (self.rects[0].centerx,self.rects[0].centery + 25), 7, 0)
