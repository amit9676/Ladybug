import math

import pygame
from InstanceClass import NPCInstance
from explosionClass import Explosion

'''rocket class, fired by ladybug (and with the option of future units).
unlike the fireball and flamethrower - the rocket is automatically guided at the target mid-flight.

when impacted or 10 seconds passed since rocket launch - the rocket will be replaced by explosion animation, however
as the explosion is bound to the rocket - it will be considered the same object, they are programmatically.'''
class Rocket:
    def __init__(self, game, caller, team, direction, emergence, logicSupport, speed=2):
        self.__image = pygame.image.load("images/rocket.png")
        self.__image = pygame.transform.scale(self.__image, (12, 28))
        self.__original = self.__image
        self.__mask = pygame.mask.from_surface(self.__image)

        self.__game = game
        self.__caller = caller #the unit that launched the rocket
        self.__logicSupport = logicSupport
        self.__npcInstance = NPCInstance(team, logicSupport)
        self.__speed = speed
        self.__target = None #as the rocket is guided at target - it needs one to begin with

        # Get the rect of the image
        self.__rect = self.__image.get_rect()
        self.__pivot = (self.__rect.width/2, self.__rect.height / 2)

        self.__emergence_x, self.__emergence_y = emergence
        self.__movement_direction = direction
        self.__rotation_angle = 0
        self.__desired_direction = 0

        self.__initilizeRocket()
        self.__current_x, self.__current_y = self.__logicSupport.initilize_currents(self.__rect.x, self.__rect.y)
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

    def get_target(self):
        return self.__target

    def __initilizeRocket(self):
        self.__current_x, self.__current_y = self.__logicSupport.initilize_currents(self.__rect.x, self.__rect.y)
        self.__winMode = False
        self.__rotation_angle = self.__logicSupport.game_to_graph_axis_degrees(self.__movement_direction)

        '''make the rocket appear on the right of the caller'''
        pos = self.__logicSupport.circular_emergernce_position((self.__emergence_x, self.__emergence_y),
                                                               (self.__rotation_angle - 90) % 360, self.__caller.get_rect().width / 2)


        self.__image, self.__rect = self.__logicSupport.blitRotate \
            (self.__image, pos, self.__pivot, self.__rotation_angle)

        '''get target, if None it return - the rocket will fly straight forward until it crosses window boundries and
        removed from game.'''
        self.__target = self.__target_acquisition()

    '''this target acquisition function is DIFFERENT than the normal target acquisition function - the normal
    function taking the first available target, this function takes the closest target based on angle - the lesser
    you need to turn for the target - the target is being prioritized.
    
    as the function is different - it will be considered a different function than the general "get_target" function,
    as for now it is only being used by the rocket - however it might be changed in the future.'''
    def __target_acquisition(self):
        lowest_turn = 60  # how far the missile may turn to locate target- valid range: 1 <= x <= 180
        target = None
        instances = []
        instances += self.__game.get_ladybugs()
        instances += self.__game.get_wagons()
        for ins in instances:
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


    def move(self):

        if self.__explosion is None: #this if condition is for the build in explodion implementation - might be removed
            if self.__target is not None:
                self.__desired_direction = self.__npcInstance.get_desired_direction(self.__target, self.__rect)
                self.__movement_direction, diff = self.__npcInstance.make_turn \
                    (self.__movement_direction, self.__desired_direction,0.5)
                self.__rotation_angle = self.__logicSupport.game_to_graph_axis_degrees(self.__movement_direction)

            '''calculation the location in which the rocket should go'''
            self.__current_x, self.__current_y, self.__rect.x, self.__rect.y = \
                self.__logicSupport.advance(self.__movement_direction, self.__speed, self.__current_x, self.__current_y)

            '''rotate the rocket according to the new location'''
            self.__image, self.__rect = self.__logicSupport.blitRotate \
                (self.__original, (self.__rect.centerx, self.__rect.centery), self.__pivot, self.__rotation_angle)

            '''rotate the mask according the new image after the rotation'''
            self.__mask = pygame.mask.from_surface(self.__image)

            '''when rocket impacts its target (or any other unit on screen) - set impact mode active and replace
            rocket animation with explosion animation'''
            impacted = self.__logicSupport.impact_identifier(self, self.__caller, self.__game.get_ladybugs()
                                                             + self.__game.get_wagons())
            if impacted:
                self.__setup_explosion()
                impacted[0].decrease_hitPoints(100)
                #print(impacted[0].get_hitpoints())

            x = pygame.time.get_ticks() - self.__timer
            if x >= 10000:
                self.__setup_explosion()
        else: #if the explosion implementation is changed - remove all else block
            if self.__explosion.self_destruct:
                self.self_destruct = True
            else:
                '''run explosion animation'''
                self.__explosion.move()
                self.__image = self.__explosion.get_image()
                temp = self.__rect.centerx, self.__rect.centery
                self.__rect = self.__image.get_rect()
                self.__rect.center = temp


    def draw(self, surface):
        # Draw the image on the surface
        #pygame.draw.rect(surface, (0, 255, 0), self.__rect, 2)
        self.__logicSupport.draw(surface, self.__image, self.__rect)

    '''sets up an explosion - basically the rocket changes to explosion animation with different behavior.
    as the explosion is bound to the rocket - the rocket class will contain an instance of explosion object as well'''
    def __setup_explosion(self):
        self.__explosion = Explosion(self.__logicSupport, (self.__rect.x, self.__rect.y))
