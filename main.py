import math
import random


'''main operations class - this class contains method which are used by multiple classes'''
class main:
    def __init__(self):
        self.__WINDOW_WIDTH = 800
        self.__WINDOW_HEIGHT = 600
        self.winMode = True

    def get_window(self):
        return self.__WINDOW_WIDTH, self.__WINDOW_HEIGHT

    def trigo(self, direction, speed, current_x, current_y):
        dx = math.sin(math.radians(direction)) * speed
        dy = math.cos(math.radians(direction)) * speed
        # Update the ladybug's position
        return current_x + dx, current_y - dy, round(current_x + dx), round(current_y - dy)


    def initilize_currents(self,x,y):
        return float(x), float(y)

    def draw(self, surface, image, rect):
        # Draw the image on the surface
        surface.blit(image, rect)


