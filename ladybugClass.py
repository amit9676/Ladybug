# ladybug.py
import pygame
import random
from fireballClass import Fireball
from main import WINDOW_WIDTH, WINDOW_HEIGHT

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

        # Set the initial speed
        self.speed = 5
        self.winMode = False
        self.initilizeGame()
        self.current_direction = 0
        self.last_shot_time = 0

    def initilizeGame(self):
        self.rect.x = random.randint(0, WINDOW_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, WINDOW_HEIGHT - self.rect.height)
        self.winMode = False

    def update(self, keys):
        if self.winMode:
            return
        # Move the ladybug based on the arrow key input
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            if keys[pygame.K_UP]:
                self.image = pygame.transform.rotate(self.original, 45)
                self.current_direction = 45
            elif keys[pygame.K_DOWN]:
                self.image = pygame.transform.rotate(self.original, 135)
                self.current_direction = 135
            else:
                self.image = pygame.transform.rotate(self.original, 90)
                self.current_direction = 90

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            if keys[pygame.K_UP]:
                self.image = pygame.transform.rotate(self.original, 315)
                self.current_direction = 315
            elif keys[pygame.K_DOWN]:
                self.image = pygame.transform.rotate(self.original, 225)
                self.current_direction = 225
            else:
                self.image = pygame.transform.rotate(self.original, 270)
                self.current_direction = 270

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            if keys[pygame.K_RIGHT]:
                self.image = pygame.transform.rotate(self.original, 315)
                self.current_direction = 315
            elif keys[pygame.K_LEFT]:
                self.image = pygame.transform.rotate(self.original, 45)
                self.current_direction = 45
            else:
                self.image = pygame.transform.rotate(self.original, 0)
                self.current_direction = 0
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            if keys[pygame.K_RIGHT]:
                self.image = pygame.transform.rotate(self.original, 225)
                self.current_direction = 225
            elif keys[pygame.K_LEFT]:
                self.image = pygame.transform.rotate(self.original, 135)
                self.current_direction = 135
            else:
                self.image = pygame.transform.rotate(self.original, 180)
                self.current_direction = 180

        #print(current_direction)
        if keys[pygame.K_SPACE]:
            self.shoot(self.current_direction,self.rect.x,self.rect.y)
        for fireball in self.fireballs:
            fireball.move()
            if fireball.self_destruct:
                self.fireballs.remove(fireball)


        # Keep the ladybug inside the window
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT

    def draw(self, surface):
        # Draw the image on the surface
        surface.blit(self.image, self.rect)

    def win(self):
        self.winMode = True
        self.rect.x = -100
        self.rect.y = -100
        self.fireballs.clear()

    def shoot(self, direction, x,y):
        current_time = pygame.time.get_ticks()
        x_val = 12
        y_val = 12

        if direction == 45 or direction == 135 or direction == 225 or direction == 315:
            x_val = 17
            y_val = 17

        if current_time - self.last_shot_time >= 333:
            self.last_shot_time = current_time
            self.fireballs.append(Fireball(direction,x,y,x_val,y_val))

