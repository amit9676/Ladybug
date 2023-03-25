import math

import pygame
import main
from main import WINDOW_WIDTH, WINDOW_HEIGHT
from spriteHandler_Class import Sprite


class Flamethrower:
    """main initlization of the flamethrower - takes the sprite, direction and x,y coordinates from external method.
    in addition initilize from vairables required for the object, such as radius, speed"""

    def __init__(self, direction, emergence_x, emergence_y):
        # self.spr = Sprite("flame001.png", 93, 216, 15, 5, 30)
        self.spr = Sprite("flame002.png", 181, 404, 10, 5, 40)
        self.image = self.spr.fill_frames_and_get_first_frame()

        self.pivot = self.spr.get_pivot()
        direction = self.__game_to_graph_axis_degrees(direction)
        self.radius = 3
        pos = [emergence_x + math.cos(math.radians(direction)) * self.radius,
               emergence_y - math.sin(math.radians(direction)) * self.radius]
        self.speed = 5  # for now speed is hardcoded, if changes - the speed needs to be an input parameter.

        self.original = self.image
        self.current_time = pygame.time.get_ticks()
        self.image, self.current_time = self.spr.update_animation_frame(self.current_time)
        self.rect = self.original.get_rect()

        self.image, self.rect = self.__blitRotate(self.original,pos,self.pivot,direction-90)
        self.self_destruct = False


    '''un used method, might be reused later'''
    def initilizeFlame(self, x, y):
        pass

    '''this method is responsible for rotating an image as we will.
    image argument its the the image we would like to rotate.
    pos is (x,y) tuple of to where place the pivot of the image.
    pivot is (x,y) tuple - the point on image that would be used as rotation anchor-the image will be rotated around it.
    angle is the rotation angle, based on mathematical axis graph.
    the output is the rotation image, and the rectangle of it.'''

    def __blitRotate(self, image, pos, pivot, angle):
        image_rect = image.get_rect(topleft=(pos[0] - pivot[0], pos[1] - pivot[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(image, angle)

        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
        return rotated_image, rotated_image_rect

    '''the method is responsible of updating the flamethrower - it gets from the outside the x and y coordinates of
    where to place the flamethrower, and a direction from which to extract the required angle for rotation'''

    def move(self, direction, x, y):
        direction = self.__game_to_graph_axis_degrees(direction)
        pos = [x + math.cos(math.radians(direction)) * self.radius, y - math.sin(math.radians(direction)) * self.radius]
        self.image, self.rect = self.__blitRotate(self.original, pos, self.pivot, direction - 90)
        self.original, self.current_time = self.spr.update_animation_frame(self.current_time)

    '''this private method is required to convert the game directions (which 0 degrees is up arrow) - to mathematical
    angles which are needed for the rotation calculations, which are based on radians, circles and trigonometry.'''

    def __game_to_graph_axis_degrees(self, direction):
        return (90 - direction) % 360

    ''' draw the flame on screen'''
    def draw(self, surface):
        # Draw the image on the surface
        surface.blit(self.image, self.rect)
