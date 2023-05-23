import pygame
import random
from ladybugPlayerClass import Ladybug_Player
from flagClass import Flag
from warWagonClass import WarWagon
from ladybugNPCClass import Ladybug_NPC
from discClass import Disc
from informationDisplayClass import InformationDisplayClass
from main import main


class Game:
    def __init__(self, size, mainActions):
        # Create the ladybug and flag objects
        self.__mainActions = mainActions
        #self.__window_size = size
        information_height_size = 100
        self.__window_size = (size[0], size[1] - information_height_size)
        self.__ladybug = Ladybug_Player(self.__window_size, self.__mainActions, self, "red")
        self.__ladybug_npc = Ladybug_NPC(self.__window_size, self.__mainActions, self, "blue")
        self.information = InformationDisplayClass((0, self.__window_size[1])
            , (self.__window_size[0],information_height_size), self.__ladybug.get_ladybug_data())

        #self.__flag = Flag(self.__window_size, self.__mainActions)
        #self.__warWagon = WarWagon(self.__window_size, self.__mainActions, self, "blue")
        #self.__disc = Disc(self.__window_size, self.__mainActions,self, "warWagon_model")

        # a list of all inctances (ladybugs, warwagons and future instances)
        self.inctances = []
        self.warWagons = []
        self.discs = []

        '''the placement of the following 2 line of codes is TEMPORARY for testing'''
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

    # def __start_initilzation(self):
    #     #pygame.init()
    #
    #     # Create the window
    #     window = pygame.display.set_mode((self.__window_size[0], self.__window_size[1]))
    #     pygame.display.set_caption("Ladybug Game")
    #     pygame_icon = pygame.image.load('ladybug_red.png')
    #     pygame.display.set_icon(pygame_icon)
    #
    #     # Set the background color
    #     background_color = (135, 206, 235)
    #     return window, background_color

    def get_window_size(self) -> (int,int):
        return self.__window_size

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

    def update(self):

        # Update the ladybug object
        keys = pygame.key.get_pressed()
        self.__ladybug.update(keys)
        self.__ladybug_npc.update()
        self.information.update(self.__ladybug.get_ladybug_data())

        '''war wagons'''
        for w in self.warWagons:
            w.update()
            if w.self_destruct and not w.fireballs:
                self.warWagons.remove(w)

        '''discs'''
        self.create_disk()
        for d in self.discs:
            d.update()
            if d.self_destruct:
                self.discs.remove(d)

        # Check if the ladybug has reached the flag
        # if self.__ladybug.get_rect().colliderect(self.__flag.get_rect()):
        #     self.__win = True
        #     self.__playing = False
        #     self.__ladybug.win()
        #     self.__ladybug_npc.win()
        #     #self.__flag.win()
        #     self.__create_button()
        #     self.__message = None
        #     self.__show_message("YOU WIN!")

    '''main draw method - in here make sure every game instance is being drown'''

    def draw(self, window):
        # Fill the window with the background color
        #window.fill(self.background)

        # if self.__disc:
        #     self.__disc.draw(self.__window)
        for d in self.discs:
            d.draw(window)

        for w in self.warWagons:
            w.draw(window)
            for fireball in w.fireballs:
                fireball.draw(window)

        # Draw the ladybug and flag on the window
        self.__ladybug.draw(window)
        #self.__flag.draw(self.__window)
        self.__ladybug_npc.draw(window)

        # if self.__warWagon:
        #     self.__warWagon.draw(self.__window)
        #     for fireball in self.__warWagon.fireballs:
        #         fireball.draw(self.__window)

        for fireball in self.__ladybug.fireballs:
            fireball.draw(window)

        for fireball in self.__ladybug_npc.fireballs:
            fireball.draw(window)

        for rocket in self.__ladybug.rockets:
            rocket.draw(window)

        for rocket in self.__ladybug_npc.rockets:
            rocket.draw(window)

        if self.__ladybug.flame:
            self.__ladybug.flame.draw(window)

        if self.__ladybug_npc.flame:
            self.__ladybug_npc.flame.draw(window)

        self.information.draw(window)

    def __reset(self):
        # Reset the game state
        self.__ladybug.initilize_instance()
        self.__ladybug_npc.initilize_instance()
        #self.__flag.initilize_instance()
        self.__message = None
        self.__button = None
        self.__win = False

    def create_disk(self):
        """default value 7500
        this method is responsible to create a disk at probablity of 1 to 7500.
        currently - there are 3 types of disk:
        war wagon - which summons war wagon to help the summoner.
        rockets ammo, and flamethrower ammo."""
        probability = 7500
        chance = random.randint(1, probability)
        #location = self.__mainActions.generate_random_location(self.__window_size)
        if chance % probability == 0:
            chance = random.randint(1, 3)
            if chance == 1:
                self.discs.append(Disc(self.__window_size, self.__mainActions,self, "warWagon_model"))
            elif chance == 2:
                self.discs.append(Disc(self.__window_size, self.__mainActions,self, "rocket", (12, 28)))
            else:
                self.discs.append(Disc(self.__window_size, self.__mainActions,self, "flame001_model"))

    def create_warWagon(self, team):
        self.warWagons.append(WarWagon(self.__window_size, self.__mainActions, self, team))
        #self.inctances.append(WarWagon(self.__window_size, self.__mainActions, self, team))

    def run(self):
        # Set the game's framerate
        framerate = 300

        while self.__running:
            # Handle events
            #self.__handle_events()

            # Update the game state
            self.update()

            # Draw the game
            self.draw()

            # Update the display
            pygame.display.update()

            # Set the framerate of the game
            self.__clock.tick(framerate)

        # Quit Pygame
        pygame.quit()


# Run the game
#game = Game()
#game.run()
