# ladybug.py
import pygame
import random

import main
from fireballClass import Fireball
from flameThrowerClass import Flamethrower
from main import WINDOW_WIDTH, WINDOW_HEIGHT
import math

# Define the Ladybug class
class Ladybug:
    def __init__(self):
        # Load the image
        self.image = pygame.image.load("ladybug.png")
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.original = self.image

        # Get the rect of the image
        self.rect = self.image.get_rect()

        self.fireballs = []
        self.flame = None

        # Set the initial speed
        self.speed = 5
        self.winMode = False
        self.initilizeGame()
        self.current_direction = 0
        self.current_x = float(self.rect.x)
        self.current_y = float(self.rect.y)
        self.last_shot_time = 0

        # Initialize forehead position and marker image
        self.forehead_offset = (-2, -self.image.get_height() // 2)
        #self.forehead_marker = pygame.Surface((5, 5))
        #self.forehead_marker.fill((255, 0, 0))

    def initilizeGame(self):
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, WINDOW_HEIGHT - self.rect.height)
        self.current_x = float(self.rect.x)
        self.current_y = float(self.rect.y)
        self.winMode = False


    def update(self, keys):
        if self.winMode:
            return
        # Move the ladybug based on the arrow key input
        if keys[pygame.K_LEFT]:
            self.current_direction = (self.current_direction - 5) % 360
            #print(f"direction: {self.current_direction}")

        if keys[pygame.K_RIGHT]:
            self.current_direction = (self.current_direction + 5) % 360
            #print(f"direction: {self.current_direction}")

        if keys[pygame.K_UP]:
            self.current_x, self.current_y, self.rect.x, self.rect.y =\
                main.trigo(self.current_direction, self.speed, self.current_x, self.current_y)



            #print(f"dx: {dx}, dy: {dy}, self.rect.x: {self.rect.x}, self.rect.y: {self.rect.y},  direction: {self.current_direction}")
            #print(f"self.current_x: {self.current_x}, self.current_y: {self.current_y}")
            #print()


        self.image = pygame.transform.rotate(self.original, -self.current_direction)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

        forehead_x, forehead_y = self.rect.centerx, self.rect.centery
        forehead_x += int(self.forehead_offset[0] * math.cos(math.radians(self.current_direction))) - int(self.forehead_offset[1] * math.sin(math.radians(self.current_direction)))
        forehead_y += int(self.forehead_offset[0] * math.sin(math.radians(self.current_direction))) + int(self.forehead_offset[1] * math.cos(math.radians(self.current_direction)))
        #self.forehead_position = (forehead_x, forehead_y)

        #print(current_direction)
        if keys[pygame.K_SPACE]:
            self.shoot(self.current_direction,center[0],
                       center[1])
        for fireball in self.fireballs:
            fireball.move()
            if fireball.self_destruct:
                self.fireballs.remove(fireball)

        if keys[pygame.K_a]:
            if self.flame is None:
                self.flame = Flamethrower(self.current_direction, forehead_x, forehead_y)
            else:
                self.flame.move(self.current_direction, forehead_x, forehead_y)

        else:
            self.flame = None



        # Keep the ladybug inside the window
        if self.rect.left < 0:
            self.rect.left = 0
            self.current_x = 0
            self.rect.x = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.current_x = WINDOW_WIDTH - self.image.get_width()
            self.rect.x = WINDOW_WIDTH - self.image.get_width()
        if self.rect.top < 0:
            self.rect.top = 0
            self.current_y = 0
            self.rect.y = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.current_y = WINDOW_HEIGHT - self.image.get_height()
            self.rect.y = WINDOW_HEIGHT - self.image.get_height()

    def draw(self, surface):
        # Draw the image on the surface
        surface.blit(self.image, self.rect)
        #surface.blit(self.forehead_marker, self.forehead_position)

    def win(self):
        self.winMode = True
        self.rect.x = -100
        self.rect.y = -100
        self.fireballs.clear()

    def shoot(self, direction, x,y):
        current_time = pygame.time.get_ticks()
        x_val = 17
        y_val = 17

        if 45 <= direction <= 135 or 225 <= direction <= 315:
            x_val = 17
            y_val = 17

        if current_time - self.last_shot_time >= 333:
            self.last_shot_time = current_time
            self.fireballs.append(Fireball(direction,x,y))

    def burn(self,direction,x,y):
        self.flame = Flamethrower(direction,x,y)

