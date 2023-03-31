import math
import pygame
import random


'''main operations class - this class contains method which are used by multiple classes'''
class main:
    def __init__(self):
        self.__WINDOW_WIDTH = 1000
        self.__WINDOW_HEIGHT = 750
        self.winMode = True

    def get_window(self):
        return self.__WINDOW_WIDTH, self.__WINDOW_HEIGHT

    def trigo(self, direction, speed, current_x, current_y):
        dx = math.sin(math.radians(direction)) * speed
        dy = math.cos(math.radians(direction)) * speed
        # Update the  position
        return current_x + dx, current_y - dy, round(current_x + dx), round(current_y - dy)


    def initilize_currents(self,x,y):
        return float(x), float(y)

    def draw(self, surface, image, rect):
        # Draw the image on the surface
        surface.blit(image, rect)


    '''this method is responsible for rotating an image as we will.
    image argument its the the image we would like to rotate.
    pos is (x,y) tuple of to where place the pivot of the image on the screen.
    pivot is (x,y) tuple - the point on image that would be used as rotation anchor-the image will be rotated around it.
    angle is the rotation angle, based on mathematical axis graph.
    the output is the rotation image, and the rectangle of it.'''
    def blitRotate(self, image, pos, pivot, angle):
        image_rect = image.get_rect(topleft=(pos[0] - pivot[0], pos[1] - pivot[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(image, angle)

        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
        return rotated_image, rotated_image_rect

    '''this private method is required to convert the game directions (which 0 degrees is up arrow) - to mathematical
    angles which are needed for the rotation calculations, which are based on radians, circles and trigonometry.'''
    def game_to_graph_axis_degrees(self, direction):
        return (90 - direction) % 360

    def check_for_boundry_crossing(self, rect):
        if rect.right < 0 or rect.left > self.__WINDOW_WIDTH or rect.bottom < 0 \
                or rect.top > self.__WINDOW_HEIGHT:
            return True
        return False

