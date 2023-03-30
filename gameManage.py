import pygame
import random
from ladybugClass import Ladybug
from flagClass import Flag
from wagonGunClass import  WagonGun
from main import main


# Initialize Pygame
# pygame.init()
#
# # Create the window
# window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# pygame.display.set_caption("Ladybug Game")
# pygame_icon = pygame.image.load('ladybug.png')
# pygame.display.set_icon(pygame_icon)
#
# # Set the background color
# background_color = (135, 206, 235)

# Define the Game class
class Game:
    def __init__(self):
        # Create the ladybug and flag objects
        self.__mainActions = main()
        self.__window_size = self.__mainActions.get_window()
        self.__window, self.background = self.__start_initilzation()
        self.__ladybug = Ladybug(self.__window_size, self.__mainActions)
        self.__flag = Flag(self.__window_size, self.__mainActions)
        self.__wagonGun = WagonGun(self.__window_size, self.__mainActions)

        # Set the game state to "running"
        self.__running = True
        self.__clock = pygame.time.Clock()
        self.__font = pygame.font.SysFont('Arial', 50)
        self.__message = None
        self.__playing = True
        self.__win = False
        self.__button = None

    def __start_initilzation(self):
        pygame.init()

        # Create the window
        window = pygame.display.set_mode((self.__window_size[0], self.__window_size[1]))
        pygame.display.set_caption("Ladybug Game")
        pygame_icon = pygame.image.load('ladybug.png')
        pygame.display.set_icon(pygame_icon)

        # Set the background color
        background_color = (135, 206, 235)
        return window, background_color

    '''main method for event handling, such as game over and stuff'''

    def __handle_events(self):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Quit the game if the user closes the window
                self.__running = False
            if event.type == pygame.MOUSEBUTTONDOWN and self.__button is not None:
                # If the player clicks on the button, reset the game
                if self.__button.collidepoint(event.pos):
                    self.__reset()

    '''update the game - in here make sure everything in the game is being updated.'''

    def __update(self):
        # Update the ladybug object
        keys = pygame.key.get_pressed()
        self.__ladybug.update(keys)

        # Check if the ladybug has reached the flag
        if self.__ladybug.get_rect().colliderect(self.__flag.get_rect()):
            self.__win = True
            self.__playing = False
            self.__ladybug.win()
            self.__flag.win()
            self.__create_button()
            self.__message = None
            self.__show_message("YOU WIN!")

    '''main draw method - in here make sure every game instance is being drown'''

    def __draw(self):
        # Fill the window with the background color
        self.__window.fill(self.background)

        # Draw the ladybug and flag on the window
        self.__ladybug.draw(self.__window)
        self.__flag.draw(self.__window)
        self.__wagonGun.draw(self.__window)

        for fireball in self.__ladybug.fireballs:
            fireball.draw(self.__window)

        if self.__ladybug.flame:
            self.__ladybug.flame.draw(self.__window)

        # Show the message if there is one
        if self.__message:
            text_surface = self.__font.render("YOU WIN", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.__message.center)
            self.__window.blit(text_surface, text_rect)

        # Draw the button
        if self.__button:
            pygame.draw.rect(self.__window, (0, 255, 0), self.__button)
            text_surface = self.__font.render("Play again", True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=self.__button.center)
            self.__window.blit(text_surface, text_rect)

        if self.__button and self.__button.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def __show_message(self, message):
        button_width = 200
        button_height = 50
        button_x = self.__window_size[0] // 2 - button_width // 2
        button_y = self.__window_size[1] // 2 - 100
        self.__message = pygame.Rect(button_x, button_y, button_width, button_height)

    def __create_button(self):
        # Create a button to restart the game
        button_width = 200
        button_height = 50
        button_x = self.__window_size[0] // 2 - button_width // 2
        button_y = self.__window_size[1] // 2
        self.__button = pygame.Rect(button_x, button_y, button_width, button_height)

    def __reset(self):
        # Reset the game state
        self.__ladybug.initilize_instance()
        self.__flag.initilize_instance()
        self.__message = None
        self.__button = None
        self.__win = False

    def run(self):
        # Set the game's framerate
        framerate = 60

        while self.__running:
            # Handle events
            self.__handle_events()

            # Update the game state
            self.__update()

            # Draw the game
            self.__draw()

            # Update the display
            pygame.display.update()

            # Set the framerate of the game
            self.__clock.tick(framerate)

        # Quit Pygame
        pygame.quit()


# Run the game
game = Game()
game.run()
