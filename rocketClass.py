import math

import pygame
from InstanceClass import NPCInstance


class Rocket:
    def __init__(self, game, team, direction, emergence, mainActions, speed=2):
        self.__image = pygame.image.load("rocket.png")
        self.__image = pygame.transform.scale(self.__image, (20, 20))
        self.__original = self.__image

        self.__game = game
        self.__mainActions = mainActions
        self.__npcInstance = NPCInstance(team, mainActions)
        self.__speed = speed
        self.__target = None

        # Get the rect of the image
        self.__rect = self.__image.get_rect()
        self.__pivot = (self.__rect.width / 2, self.__rect.height / 2)

        self.__emergence_x, self.__emergence_y = emergence
        self.__movement_direction = direction
        self.__rotation_angle = 0
        self.__desired_direction = 0
        self.__initilizeRocket()
        self.__current_x, self.__current_y = self.__mainActions.initilize_currents(self.__rect.x, self.__rect.y)
        self.self_destruct = False
        self.__winMode = False

    def __initilizeRocket(self):
        # self.__rect.centerx = self.__emergence_x
        # self.__rect.centery = self.__emergence_y
        self.__current_x, self.__current_y = self.__mainActions.initilize_currents(self.__rect.x, self.__rect.y)
        self.__winMode = False
        self.__rotation_angle = self.__mainActions.game_to_graph_axis_degrees(self.__movement_direction)
        self.__image, self.__rect = self.__mainActions.blitRotate \
            (self.__image, (self.__emergence_x, self.__emergence_y), self.__pivot, self.__rotation_angle)
        self.__target = self.__target_acqesition()

    def __target_acqesition(self):
        lowest_turn = 90
        target = None
        for ins in self.__game.inctances:
            if ins.get_instance_struct().get_team() == self.__npcInstance.get_team():
                continue
            diff = \
                self.__npcInstance.get_desired_direction(ins, self.__rect) - self.__movement_direction
            if diff > 180:
                diff -= 360
            elif diff < -180:
                diff += 360
            diff=abs(diff)
            print(f"direction from me to target: {self.__npcInstance.get_desired_direction(ins, self.__rect)}, "
                  f"where i am heading: {self.__movement_direction}")
            print(f"distance_of_current_direction_and_desired_direction:"
                  f" {diff}\n")
            if diff < lowest_turn:
                lowest_turn = diff
                target = ins

        if not target:
            return None
        #self.__target = self.__npcInstance.get_target(self.__game)
        return target

    '''move fireball at the pre determined path'''

    def move(self):
        if self.__target is not None:
            self.__desired_direction = self.__npcInstance.get_desired_direction(self.__target,self.__rect)
            self.__movement_direction, diff = self.__npcInstance.make_turn\
                (self.__movement_direction, self.__desired_direction)
            self.__rotation_angle = self.__mainActions.game_to_graph_axis_degrees(self.__movement_direction)
        # self.__desired_direction = self.__npcInstance.get_desired_direction(self.__target,self.__rect.center)
        self.__current_x, self.__current_y, self.__rect.x, self.__rect.y = \
            self.__mainActions.advance(self.__movement_direction, self.__speed, self.__current_x, self.__current_y)

        self.__image, self.__rect = self.__mainActions.blitRotate \
            (self.__original, (self.__current_x, self.__current_y), self.__pivot, self.__rotation_angle)

        if self.__mainActions.check_for_boundary_crossing(self.__rect):
            self.self_destruct = True

    def draw(self, surface):
        # Draw the image on the surface
        self.__mainActions.draw(surface, self.__image, self.__rect)
        # pygame.draw.rect(surface, (140, 140, 21), self.__rect, 2)
