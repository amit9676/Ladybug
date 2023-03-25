import math

import pygame
import main
from main import WINDOW_WIDTH, WINDOW_HEIGHT
from spriteTest import Sprite


class Flamethrower:
    def __init__(self, direction, emergence_x, emergence_y):
        #self.spr = Sprite("flame001.png", 93, 216, 15, 5, 30)
        self.spr = Sprite("flame002.png", 181, 404, 10, 5, 40)
        self.image = self.spr.fill_frames_and_get_first_frame()

        self.pivot = self.spr.get_pivot()
        direction = self.__game_to_graph_axis_degrees(direction)
        self.radius = -5
        pos = [emergence_x + math.cos(math.radians(direction))*self.radius,
               emergence_y - math.sin(math.radians(direction))*self.radius]
        self.speed = 5
        self.original = self.image
        self.current_time = pygame.time.get_ticks()
        self.image, self.current_time = self.spr.update_animation_frame(self.current_time)
        self.rect = self.original.get_rect()



        #self.original, self.rect = self.blitRotate(self.original,pos,self.pivot,direction-90)
        self.self_destruct = False


    def initilizeFlame(self,x,y):
        pass


    def blitRotate(self, image, pos, originPos, angle):
        image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(image, angle)

        rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
        return rotated_image, rotated_image_rect

    def move(self, direction, x, y):
        direction = self.__game_to_graph_axis_degrees(direction)
        pos = [x + math.cos(math.radians(direction))*self.radius, y - math.sin(math.radians(direction))*self.radius]
        self.image, self.rect = self.blitRotate(self.original,pos,self.pivot,direction-90)
        self.original, self.current_time = self.spr.update_animation_frame(self.current_time)



    def __game_to_graph_axis_degrees(self,direction):
        return (90 - direction) % 360


    def draw(self, surface):
        # Draw the image on the surface
        surface.blit(self.image, self.rect)

