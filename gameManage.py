import pygame
import random
from ladybugClass import Ladybug
from flagClass import Flag
from main import WINDOW_WIDTH, WINDOW_HEIGHT

# Initialize Pygame
pygame.init()

# Create the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ladybug Game")
pygame_icon = pygame.image.load('ladybug.png')
pygame.display.set_icon(pygame_icon)

# Set the background color
background_color = (135, 206, 235)

# Define the Game class
class Game:
    def __init__(self):
        # Create the ladybug and flag objects
        self.ladybug = Ladybug()
        self.flag = Flag()

        # Set the game state to "running"
        self.running = True
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 50)
        self.message = None
        self.playing = True
        self.win = False
        self.button = None

    '''main method for event handling, such as game over and stuff'''
    def handle_events(self):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game if the user closes the window
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.button is not None:
                # If the player clicks on the button, reset the game
                if self.button.collidepoint(event.pos):
                    self.reset()

    '''update the game - in here make sure everything in the game is being updated.'''
    def update(self):
        # Update the ladybug object
        keys = pygame.key.get_pressed()
        self.ladybug.update(keys)

        # Check if the ladybug has reached the flag
        if self.ladybug.rect.colliderect(self.flag.rect):
            self.win = True
            self.playing = False
            self.ladybug.win()
            self.flag.win()
            self.create_button()
            self.message = None
            self.show_message("YOU WIN!")

    '''main draw method - in here make sure every game instance is being drown'''
    def draw(self):
        # Fill the window with the background color
        window.fill(background_color)

        # Draw the ladybug and flag on the window
        self.ladybug.draw(window)
        self.flag.draw(window)

        for fireball in self.ladybug.fireballs:
            fireball.draw(window)

        if self.ladybug.flame:
            self.ladybug.flame.draw(window)


        # Show the message if there is one
        if self.message:
            text_surface = self.font.render("YOU WIN", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.message.center)
            window.blit(text_surface, text_rect)

        # Draw the button
        if self.button:
            pygame.draw.rect(window, (0, 255, 0), self.button)
            text_surface = self.font.render("Play again", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.button.center)
            window.blit(text_surface, text_rect)

        if self.button and self.button.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def show_message(self, message):
        button_width = 200
        button_height = 50
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        button_y = WINDOW_HEIGHT // 2 - 100
        self.message = pygame.Rect(button_x, button_y, button_width, button_height)

    def create_button(self):
        # Create a button to restart the game
        button_width = 200
        button_height = 50
        button_x = WINDOW_WIDTH // 2 - button_width // 2
        button_y = WINDOW_HEIGHT // 2
        self.button = pygame.Rect(button_x, button_y, button_width, button_height)

    def reset(self):
        # Reset the game state
        self.ladybug.initilizeGame()
        self.flag.initilizeGame()
        self.message = None
        self.button = None
        self.win = False

    def run(self):
        # Set the game's framerate
        framerate = 60

        while self.running:
            # Handle events
            self.handle_events()

            # Update the game state
            self.update()

            # Draw the game
            self.draw()

            # Update the display
            pygame.display.update()

            # Set the framerate of the game
            self.clock.tick(framerate)

        # Quit Pygame
        pygame.quit()


# Run the game
game = Game()
game.run()
