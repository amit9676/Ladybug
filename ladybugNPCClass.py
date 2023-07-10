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
    """initialize the ladybug with necessary parameters"""

    def __init__(self, window, logicSupport, game, team):
        super().__init__(window, logicSupport, game, team)

        '''which instance this instance is targeting at any moment'''
        self._instance_struct: NPCInstance = NPCInstance(team, logicSupport)
        self.__target = None
        self.__desired_direction = self.get_instance_struct().get_desired_direction(self.__target, self.get_rect())
        self.__evasive_maneuver = False
        self.__evasive_maneuver_timer = 0


        self.__advanced = False
        # self.__evasive_maneuver_counter = 0
        # self.__evasive_maneuver_angle = 0

    # def decrease_hitPoints(self, amount: int):
    #     super().decrease_hitPoints(amount)

    def __advance(self):
        if not self.__advanced:
            self._current_x, self._current_y, self.get_rect().x, self.get_rect().y = self._logicSupport.advance(self._current_direction, self._speed, self._current_x, self._current_y)
            self._current_speed = self._speed
            self.__advanced = True

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

    def flamethrower_hit(self):
        self.__evasive_maneuver = True
        self.__evasive_maneuver_timer = pygame.time.get_ticks()

    def __attack_ladybug(self, diff: int, distance):

        if self._flamethrower > 0:
            if distance <= self._logicSupport.get_flamethrower_range():
                self.shoot_flamethrower()
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

    # def __perform_evasive_maneuver(self):
    #     self.flame = None
    #     self.__evasive_maneuver_counter += 1
    #     if self.__evasive_maneuver_counter % 3000 == 0:
    #         self.__evasive_maneuver_angle += 1
    #         self._current_direction = (self._current_direction + self.__evasive_maneuver_angle) % 360
    #         self._rotate_image()
    #     if self.__evasive_maneuver_counter >= 2000:
    #         self.__evasive_maneuver_counter = 0
    #         self.__evasive_maneuver_angle = 0
    #         self.__evasive_maneuver = False

    '''the main ladybug method - check for any keyboard input and updates the ladybug according.
    the input includes movement and weapon using.'''

    def update(self):
        '''update super function, keep as is'''
        if super().update():
            return

        self.__stop_advance()
        self.__advanced = False

        '''get target, may modify'''
        self.__target = self.get_instance_struct().acquire_target(self._game) #mark opponent ladybug as target
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
        if self.__evasive_maneuver:
            self.__desired_direction = (self.__desired_direction + 180) % 360
            self.flame = None
            self.__advance()
            current_time = pygame.time.get_ticks()
            if current_time - self.__evasive_maneuver_timer >= 300:
                print("evasive maneuver off")
                self.__evasive_maneuver = False
        self._current_direction,diff = self.get_instance_struct().make_turn(self._current_direction,self.__desired_direction)
        #diff - the range between current direction and desired direction
        self._rotate_image()

        distance = self.get_instance_struct().calculate_distance(self.__target, self.get_rect())


        '''main actions - fill this'''
        if self._game.get_wagons():
            for w in self._game.get_wagons():
                if w.get_instance_struct().get_team() != self.get_instance_struct().get_team():
                    self.__advance()
                    break

        if self._game.get_ladybugs():
            for l in self._game.get_ladybugs():
                if l.get_instance_struct().get_team() != self.get_instance_struct().get_team():
                    for r in l.rockets:
                        if r.get_target() == self:
                            print("incoming rocket")
                            self.__advance()
                            break


        if not self.__evasive_maneuver:
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

