import math

import pygame
from InstanceClass import NPCInstance
from explosionClass import Explosion


class Rocket:
    def __init__(self, game, caller, team, direction, emergence, mainActions, speed=2):
        self.__image = pygame.image.load("rocket.png")
        self.__image = pygame.transform.scale(self.__image, (12, 28))
        self.__original = self.__image
        self.__mask = pygame.mask.from_surface(self.__image)

        self.__game = game
        self.__caller = caller #the unit that launched the rocket
        self.__mainActions = mainActions
        self.__npcInstance = NPCInstance(team, mainActions)
        self.__speed = speed
        self.__target = None

        # Get the rect of the image
        self.__rect = self.__image.get_rect()
        self.__pivot = (self.__rect.width/2, self.__rect.height / 2)

        self.__emergence_x, self.__emergence_y = emergence
        self.__movement_direction = direction
        self.__rotation_angle = 0
        self.__desired_direction = 0

        self.__initilizeRocket()
        self.__current_x, self.__current_y = self.__mainActions.initilize_currents(self.__rect.x, self.__rect.y)
        self.self_destruct = False
        self.__winMode = False

        self.__timer = pygame.time.get_ticks()

        '''this field is for attached explosion, might be removed with better explosion implementation'''
        self.__explosion = None

    def get_rect(self) -> pygame.rect:
        return self.__rect

    def get_mask(self) -> pygame.rect:
        return self.__mask

    def get_rocket_explosion(self) -> pygame.rect:
        return self.__explosion

    def __initilizeRocket(self):
        self.__current_x, self.__current_y = self.__mainActions.initilize_currents(self.__rect.x, self.__rect.y)
        self.__winMode = False
        self.__rotation_angle = self.__mainActions.game_to_graph_axis_degrees(self.__movement_direction)

        '''make the rocket appear on the right of the caller'''
        pos = self.__mainActions.circular_emergernce_position((self.__emergence_x, self.__emergence_y),
                                    (self.__rotation_angle - 90) % 360,self.__caller.get_rect().width/2)


        self.__image, self.__rect = self.__mainActions.blitRotate \
            (self.__image, pos, self.__pivot, self.__rotation_angle)
        self.__target = self.__target_acquisition()

    '''this target acquisition function is DIFFERENT than the normal target acquisition function - the normal
    function taking the first available target, this function takes the closest target based on angle - the lesser
    you need to turn for the target - the target is being prioritized.
    
    as the function is different - it will be consideted a different function than the general "get_target" function,
    as for now it is only being used by the rocket - however it might be changed in the future.'''
    def __target_acquisition(self):
        lowest_turn = 60  # how far the missile may turn to locate target- valid range: 1 <= x <= 180
        target = None
        for ins in self.__game.inctances:
            if ins.get_instance_struct().get_team() == self.__npcInstance.get_team():
                continue

            cur, diff = self.__npcInstance.make_turn(self.__movement_direction,
                                                     self.__npcInstance.get_desired_direction(ins, self.__rect))
            diff = abs(diff)

            if diff < lowest_turn:
                lowest_turn = diff
                target = ins

        if not target:
            return None
        return target


    '''move fireball at the pre determined path'''

    def move(self):

        if self.__explosion is None: #this if condition is for the build in explodion implementation - might be removed
            if self.__target is not None:
                self.__desired_direction = self.__npcInstance.get_desired_direction(self.__target, self.__rect)
                self.__movement_direction, diff = self.__npcInstance.make_turn \
                    (self.__movement_direction, self.__desired_direction,0.5)
                self.__rotation_angle = self.__mainActions.game_to_graph_axis_degrees(self.__movement_direction)

            '''calculation the location in which the rocket should go'''
            self.__current_x, self.__current_y, self.__rect.x, self.__rect.y = \
                self.__mainActions.advance(self.__movement_direction, self.__speed, self.__current_x, self.__current_y)

            '''rotate the rocket according to the new location'''
            self.__image, self.__rect = self.__mainActions.blitRotate \
                (self.__original, (self.__rect.centerx, self.__rect.centery), self.__pivot, self.__rotation_angle)

            '''rotate the mask according the new image after the rotation'''
            self.__mask = pygame.mask.from_surface(self.__image)

            impacted = self.__mainActions.impact_identifier(self, self.__caller, self.__game)
            if impacted:
                self.__setup_explosion()

            x = pygame.time.get_ticks() - self.__timer
            if x >= 10000:
                self.__setup_explosion()
        else: #if the explosion implementation is changed - remove all else block
            if self.__explosion.self_destruct:
                self.self_destruct = True
            else:
                self.__explosion.move()
                self.__image = self.__explosion.get_image()
                temp = self.__rect.centerx, self.__rect.centery
                self.__rect = self.__image.get_rect()
                self.__rect.center = temp


    def draw(self, surface):
        # Draw the image on the surface
        #pygame.draw.rect(surface, (0, 255, 0), self.__rect, 2)
        self.__mainActions.draw(surface, self.__image, self.__rect)

    def __setup_explosion(self):
        self.__explosion = Explosion(self.__mainActions,(self.__rect.x,self.__rect.y))
