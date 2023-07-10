# ladybug.py
import math

import pygame
import random

from fireballClass import Fireball
from ladybugClass import Ladybug
from flameThrowerClass import Flamethrower
from InstanceClass import NPCInstance


# Define the Ladybug class
'''npc ladybug class - inherent from ladybug class and contains actions and fields which are for computer controlled
lady bug'''
class Ladybug_NPC(Ladybug):
    """initilize the ladybug with necessary parameters"""

    def __init__(self, window, logicSupport, game, team):
        super().__init__(window, logicSupport, game, team)

        '''which inctance this inctance is targeting at any moment'''
        self._instance_struct: NPCInstance = NPCInstance(team, logicSupport)
        self.__target = None
        self.__desired_direction = self.get_instance_struct().get_desired_direction(self.__target, self.get_rect())
        self.__evasive_maneuver = False


    def decrease_hitPoints(self, amount: int):
        super().decrease_hitPoints(amount)
        self.__evasive_maneuver = True

    def __advance(self):
        self._current_x, self._current_y, self.get_rect().x, self.get_rect().y = self._logicSupport.advance(self._current_direction, self._speed, self._current_x, self._current_y)
        self._current_speed = self._speed

    def __advance_on_some_conditions(self, diff: int, distance):
        if distance < 30:
            return
        if distance < 80:
            if diff < 15:
                self.__advance()
        else:
            self.__advance()

    def __stop_advance(self):
        self._current_speed = 0

    def __attack_ladybug(self, diff: int, distance):

        if self._flamethrower > 0:
            if distance <= self._logicSupport.get_flamethrower_range():
                self.manage_flamethrower()
                self.__advance_on_some_conditions(diff, distance)
            else:
                self.__advance_on_some_conditions(diff, distance)
                self.flame = None
                if self._rockets > 0:
                    self.get_instance_struct().launch_rocket(self, self._current_direction, self.get_rect().center)
                else:
                    self.get_instance_struct().shoot(self._game, self, self._current_direction, self.get_rect().center)
        else:
            self.flame = None
            if self._rockets > 0:
                self.get_instance_struct().launch_rocket(self, self._current_direction, self.get_rect().center)
            else:
                self.get_instance_struct().shoot(self._game, self, self._current_direction, self.get_rect().center)


    '''the main ladybug method - check for any keyboard input and updates the ladybug according.
    the input includes movement and weapon using.'''

    def update(self):
        '''update super function, keep as is'''
        if super().update():
            return

        self.__stop_advance()

        '''get target, ,may modify'''
        self.__target = self.get_instance_struct().get_target(self._game) #mark opponent ladybug as target
        if self._game.get_discs():
            '''take the nearest disc'''
            min_distance = self.get_instance_struct().calculate_distance(self._game.get_discs()[0], self.get_rect())
            for d in self._game.get_discs():
                '''if the disc is some ammunition that the ladybug has plenty of - it wont go for it
                and prioritize other missions.'''
                if d.get_model() == "rocket" and self._rockets >= 7:
                    continue
                if d.get_model() == "flame001_model" and self._flamethrower >= 2500:
                    continue
                current_distance = self.get_instance_struct().calculate_distance(d, self.get_rect())
                if current_distance <= min_distance:
                    min_distance = current_distance
                    self.__target = d

            '''if there is some disc on screen - prioritize disc obtaining over shooting ladybug'''

        '''turn toward the target, may modify'''
        self.__desired_direction = self.get_instance_struct().get_desired_direction(self.__target, self.get_rect())
        self._current_direction,diff = self.get_instance_struct().make_turn(self._current_direction,self.__desired_direction)
        #diff - the range between current direction and desired direction
        self._rotate_image()

        distance = self.get_instance_struct().calculate_distance(self.__target, self.get_rect())


        '''main actions - fill this'''
        if self.__target.get_type() == "ladybug":
            self.__attack_ladybug(diff, distance)
        elif self.__target.get_type() == "disc":
            self.flame = None
            self.__advance_on_some_conditions(diff, distance)





        '''updating velocity, keep as it'''
        vel = self._logicSupport.calculate_velocity(self._current_speed,
                                                    self._logicSupport.game_to_graph_axis_degrees(self._current_direction))
        self._velocity[0], self._velocity[1] = vel[0], vel[1]

        '''Keep the ladybug inside the window'''
        self._boundary_keeping()

        '''update rockets and firball, keep as is.'''
        self.get_instance_struct().update_rockets(self)
        self.get_instance_struct().update_fireballs(self)

