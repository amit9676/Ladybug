import math
import random

import pygame

from fireballClass import Fireball

'''this class is instance class - it holds values and methods required by the various units in this game
this class is NOT hereditary based but encapsulation based, means in every units there is a field
of either this class, or the child class. that is because not every unit of it is using every method in it.
so to keep things precise - the connection of Instance classes and the units who use this is encapsulation based.'''


class Instance:
    def __init__(self, team, logicSupport):
        self._team = team
        self._logicSupport = logicSupport


    def get_team(self):
        return self._team

    '''weapons firing section'''

    '''shoting sections - these function responsible for shooting fireballs'''
    def shoot(self,game, caller, direction, emergernce_pos, speed=2, rate_of_fire=333):
        current_time = pygame.time.get_ticks() + rate_of_fire

        if current_time - caller._last_shot_time >= rate_of_fire:
            caller._last_shot_time = current_time
            caller.fireballs.append(Fireball(game, caller, direction, emergernce_pos, self._logicSupport, speed))
            '''add new fireball instance to the fireball list'''

    def update_fireballs(self, caller):
        for fireball in caller.fireballs:
            fireball.move()  # update fireball
            if fireball.self_destruct:
                '''for every game update we check if fireball has crossed the boundries,
                if so - the fireball is destroyed and removed from list and game memory.'''
                caller.fireballs.remove(fireball)
    '''end of shooting section'''

    '''launch rockets section'''
    def launch_rocket(self,caller, direction, emergernce_pos, speed=2, rate_of_fire=2000):
        current_time = pygame.time.get_ticks()
        if current_time - caller._last_rocket_shot_time >= rate_of_fire:
            caller._last_rocket_shot_time = current_time
            caller.fire_rocket()

    def update_rockets(self, caller):
        for rocket in caller.rockets:
            rocket.move()  # update rocket
            if rocket.self_destruct:
                caller.rockets.remove(rocket)

    # def add_rockets(self, caller):
    #     amount = random.randint(3, 10)
    #     caller.fire_rocket(amount)
    '''end of rockets section'''

    '''end of weapons sections'''

    def turn(self,current_direction,degree):
        #positive degree - turn right, negative degree - turn left.
        return (current_direction + degree) % 360


'''this is an NPC instance class - a child class of Instance - which holds common fields and actions for all NPC
instances such as npc lady bugs, war wagon and more'''


class NPCInstance(Instance):
    def __init__(self, team, logicSupport):
        super().__init__(team, logicSupport)


    '''npc section - the method below are for npc units only.'''
    '''this method is responsible for the NPC to acquire a target to attack'''

    '''get target function'''
    def get_target(self, game):
        for ins in game.get_inctances():
            if ins.get_instance_struct().get_team() != self.get_team():
                return ins
        return None

    '''get the x.y distance between you and your target'''
    def __you_and_target(self, you: pygame.rect, target: pygame.rect) -> (int, int) or (None, None):
        if target is None:
            return None, None
        dx = you.centerx - target.get_current_location()[0]
        dy = you.centery - target.get_current_location()[1]
        return dx, dy

    '''get the direction (game bases) from you to your target'''
    def get_desired_direction(self, target: pygame.rect, you: pygame.rect) -> int or None:
        dx, dy = self.__you_and_target(you, target)
        if dx is None:
            return None

        angle = math.atan2(dy, dx)
        direction = math.degrees(angle) % 360
        direction = int(direction)
        direction = (direction - 90) % 360
        return direction

    def calculate_distance(self, target: pygame.rect, rect: pygame.rect) -> int or None:
        dx, dy = self.__you_and_target(rect, target)
        if dx is None:
            return None
        return int(math.sqrt(dx ** 2 + dy ** 2))



    def make_turn(self, current_dir: int, desired_dir: int, degree=1) -> (int, int):

        # If the current and desired direction are the same, return None
        #print(f"current_dir: {current_dir}, desired_dir: {desired_dir}")
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
            #current_dir = self.turn_right(current_dir)
            current_dir = self.turn(current_dir,degree)
        else:
            #current_dir = self.turn_left(current_dir)
            current_dir = self.turn(current_dir,degree * -1)

        return current_dir, diff

    '''improved aiming function that is capable of aiming on moving target in LINEAR direction, currently used by
        war wagon, might be changed later on.
        it was made with the help of:
        https://stackoverflow.com/questions/2248876/2d-game-fire-at-a-moving-target-by-predicting-intersection-of-projectile-and-u
        '''
    def whereToShoot(self, projectile_speed, shooter_location, current_target_location, current_target_velocity):
        # Calculate the coefficients of the quadratic equation
        target_velocityX, target_velocityY = current_target_velocity

        a = target_velocityX**2 + target_velocityY**2 - projectile_speed**2
        b = 2 * (target_velocityX * (current_target_location[0] - shooter_location[0]) +
                 target_velocityY * (current_target_location[1] - shooter_location[1]))
        c = (current_target_location[0] - shooter_location[0])**2 + (current_target_location[1] - shooter_location[1])**2

        # Calculate the discriminant
        discriminant = b**2 - 4 * a * c

        # Check if a solution is possible
        if discriminant < 0:
            return None  # No solution, cannot hit the target

        # Calculate the two candidate solutions
        t1 = (-b + math.sqrt(discriminant)) / (2 * a)
        t2 = (-b - math.sqrt(discriminant)) / (2 * a)

        # Choose the smaller positive solution
        t = min(t1, t2)
        if t < 0:
            t = max(t1,t2)


        # Calculate the coordinates of the leading point to aim at
        estimated_target_x = t * target_velocityX + current_target_location[0]
        estimated_target_y = t * target_velocityY + current_target_location[1]

        # Calculate the direction in which to shoot
        dx = estimated_target_x - shooter_location[0]
        dy = (estimated_target_y - shooter_location[1]) *-1
        direction_in_radians = math.atan2(dy, dx)
        direction_in_degrees = math.degrees(direction_in_radians)
        direction_in_degrees = int(direction_in_degrees)
        direction_in_degrees = (direction_in_degrees + 360) % 360  # Convert negative angles to positive range

        # Convert the direction to pygame coordinates (0 is up, 90 is right, 180 is down, 270 is left)
        pygame_direction = self._logicSupport.game_to_graph_axis_degrees(direction_in_degrees)

        return pygame_direction


    '''draft moving target aiming. function, will be kept for now'''
    # def whereToShot(self, projectile_speed, shooter_location, current_target_location, current_target_direction, current_target_speed):
    #     # Calculate the distance between the shooter and the target
    #     dx = current_target_location[0] - shooter_location[0]
    #     dy = current_target_location[1] - shooter_location[1]
    #
    #     target_distance = math.sqrt(dx**2 + dy**2)
    #
    #     # Calculate the time it would take for the projectile to reach the target
    #     time_to_reach = target_distance / projectile_speed
    #     print(time_to_reach)
    #
    #     # Estimate the future position of the target based on its current position, direction, and speed
    #     current_target_direction = self._logicSupport.game_to_graph_axis_degrees(current_target_direction)
    #     estimated_target_x = current_target_location[0] + current_target_speed * time_to_reach * math.cos(math.radians(current_target_direction))
    #     estimated_target_y = current_target_location[1] - current_target_speed * time_to_reach * math.sin(math.radians(current_target_direction))
    #
    #     if estimated_target_x < 0:
    #         estimated_target_x = 0
    #     if estimated_target_x > self._logicSupport.get_window()[0]:
    #         estimated_target_x = self._logicSupport.get_window()[0]
    #     if estimated_target_y < 0:
    #         estimated_target_y = 0
    #     if estimated_target_y > self._logicSupport.get_window()[1] - 100:
    #         estimated_target_y = self._logicSupport.get_window()[1] - 100
    #
    #     # Calculate the direction in which to shoot
    #     dx_estimated = estimated_target_x - shooter_location[0]
    #     dy_estimated = shooter_location[1] - estimated_target_y
    #     direction_in_radians = math.atan2(dy_estimated, dx_estimated)
    #     direction_in_degrees = math.degrees(direction_in_radians)
    #     direction_in_degrees = int(direction_in_degrees)
    #     #direction_in_degrees = (direction_in_degrees + 360) % 360  # Convert negative angles to positive range
    #     #print(direction_in_degrees)
    #     # print(direction_in_degrees)
    #     # print((90 - direction_in_degrees) % 360)
    #     # print("-----------------------------------")
    #
    #     # Convert the direction to pygame coordinates (0 is up, 90 is right, 180 is down, 270 is left)
    #     pygame_direction = self._logicSupport.game_to_graph_axis_degrees(direction_in_degrees)
    #
    #     return pygame_direction
