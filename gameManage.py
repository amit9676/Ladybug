import pygame
import random
from ladybugPlayerClass import Ladybug_Player
from flagClass import Flag
from warWagonClass import  WarWagon
from ladybugNPCClass import Ladybug_NPC
from main import main


# Initialize Pygame
# pygame.init()
#
# # Create the window
# window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
# pygame.display.set_caption("Ladybug Game")
# pygame_icon = pygame.image.load('ladybug_red.png')
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
        self.__ladybug = Ladybug_Player(self.__window_size, self.__mainActions, self, "red")
        self.__ladybug_npc = Ladybug_NPC(self.__window_size, self.__mainActions, self, "blue")

        self.__flag = Flag(self.__window_size, self.__mainActions)
        self.__warWagon = WarWagon(self.__window_size, self.__mainActions, self, "blue")

        #a list of all inctances (ladybugs, warwagons and future instances)
        self.inctances = []

        '''the placement of the following 2 line of codes is TEMPORARY for testing'''
        self.inctances.append(self.__warWagon)
        self.inctances.append(self.__ladybug)
        self.inctances.append(self.__ladybug_npc)
        ''' until here'''





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
        pygame_icon = pygame.image.load('ladybug_red.png')
        pygame.display.set_icon(pygame_icon)

        # Set the background color
        background_color = (135, 206, 235)
        return window, background_color



    '''this method compiles a list of all actives instances on the game - that include player controlled ladybugs,
    NPC ladybugs, war wagon and future instances. this method has to be PUBLIC in order for the "players" to receive
    real time data about other players - instances, and their current location. all inctances must have a public method
    "get_current_location()" in order for every instance to "read the map"'''
    def get_inctances(self):
        pass

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
        self.__ladybug_npc.update()

        '''war wagons'''

        '''update if war wagon still exists'''
        if self.__warWagon is not None:
            self.__warWagon.update()
            if self.__warWagon.self_destruct:
                self.inctances.remove(self.__warWagon)
                self.__warWagon = None

        # Check if the ladybug has reached the flag
        if self.__ladybug.get_rect().colliderect(self.__flag.get_rect()):
            self.__win = True
            self.__playing = False
            self.__ladybug.win()
            self.__ladybug_npc.win()
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
        self.__ladybug_npc.draw(self.__window)

        if self.__warWagon:
            self.__warWagon.draw(self.__window)
            for fireball in self.__warWagon.fireballs:
                fireball.draw(self.__window)


        for fireball in self.__ladybug.fireballs:
            fireball.draw(self.__window)

        for fireball in self.__ladybug_npc.fireballs:
            fireball.draw(self.__window)

        if self.__ladybug.flame:
            self.__ladybug.flame.draw(self.__window)

        if self.__ladybug_npc.flame:
            self.__ladybug_npc.flame.draw(self.__window)

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
        self.__ladybug_npc.initilize_instance()
        self.__flag.initilize_instance()
        self.__message = None
        self.__button = None
        self.__win = False

    def run(self):
        # Set the game's framerate
        framerate = 300

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
