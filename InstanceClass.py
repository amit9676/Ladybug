import math

import pygame

from fireballClass import Fireball

'''this class is instance class - it holds values and methods required by the various units in this game
this class is NOT hereditary based but encapsulation based, means in every units there is a field
of either this class, or the child class. that is because not every unit of it is using every method in it.
so to keep things precise - the connection of Instance classes and the units who use this is encapsulation based.'''


class Instance:
    def __init__(self, team, mainActions):
        self._team = team
        self._last_shot_time = 0
        self.fireballs = []
        self.__mainActions = mainActions


    def get_team(self):
        return self._team

    def shoot(self, direction, x, y, speed=2, rate_of_fire=333):
        current_time = pygame.time.get_ticks()

        if current_time - self._last_shot_time >= rate_of_fire:
            self._last_shot_time = current_time
            self.fireballs.append(Fireball(direction, x, y, self.__mainActions, speed))
            '''add new fireball instance to the fireball list'''

    def update_fireballs(self):
        for fireball in self.fireballs:
            fireball.move()  # update fireball
            if fireball.self_destruct:
                '''for every game update we check if fireball has crossed the boundries,
                if so - the fireball is destroyed and removed from list and game memory.'''
                self.fireballs.remove(fireball)


    '''def get_rect(self):
        return self._rect

    def get_current_location(self):
        return self._rect.centerx, self._rect.centery'''


'''this is an NPC instance class - a child class of Instance - which holds common fields and actions for all NPC
instances such as npc lady bugs, war wagon and more'''


class NPCInstance(Instance):
    def __init__(self, team, mainActions):
        super().__init__(team, mainActions)
        #self.__target = None
        #self.__desired_direction = self.__get_desired_direction()


    '''npc section - the method below are for npc units only.'''
    '''this method is responsible for the NPC to acquire a target to attack'''

    def get_target(self, game):
        for ins in game.inctances:
            if ins.get_instance_struct().get_team() != self.get_team():
                return ins
        return None

    def __you_and_target(self, rect, target):
        if target is None:
            return None, None
        dx = rect.centerx - target.get_current_location()[0]
        dy = rect.centery - target.get_current_location()[1]
        #print(f"dx, dy: {target.get_current_location()[0]}, {target.get_current_location()[1]}")
        return dx, dy

    def get_desired_direction(self, target, rect):
        dx, dy = self.__you_and_target(rect, target)
        if dx is None:
            return None

        angle = math.atan2(dy, dx)
        direction = math.degrees(angle) % 360
        direction = int(direction)
        direction = (direction - 90) % 360
        return direction

    def calculate_distance(self, target, rect):
        dx, dy = self.__you_and_target(rect, target)
        if dx is None:
            return
        return int(math.sqrt(dx ** 2 + dy ** 2))

    def turn_right(self, current_direction):
        return (current_direction + 1) % 360

    def turn_left(self, current_direction):
        return (current_direction - 1) % 360

    def make_turn(self, current_dir, desired_dir):
        #current_dir = self._current_direction
        #desired_dir = self.__desired_direction
        #print(desired_dir)

        # If the current and desired direction are the same, return None
        if current_dir == desired_dir:
            return current_dir, 0

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
            current_dir = self.turn_right(current_dir)
        else:
            current_dir = self.turn_left(current_dir)

        return current_dir, diff
