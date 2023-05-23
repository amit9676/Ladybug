import pygame
import random
from ladybugPlayerClass import Ladybug_Player
from flagClass import Flag
from warWagonClass import WarWagon
from ladybugNPCClass import Ladybug_NPC
from discGameClass import DiscGame
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
        self.information = InformationDisplayClass((0, self.__window_size[1]), self.__mainActions
            , (self.__window_size[0],information_height_size), self.__ladybug.get_ladybug_data())


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
        self.__playing = True
        self.__win = False


    def get_window_size(self) -> (int,int):
        return self.__window_size

    '''this method compiles a list of all actives instances on the game - that include player controlled ladybugs,
    NPC ladybugs, war wagon and future instances. this method has to be PUBLIC in order for the "players" to receive
    real time data about other players - instances, and their current location. all inctances must have a public method
    "get_current_location()" in order for every instance to "read the map"'''

    def get_inctances(self):
        pass


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
        #self.__ladybug.initilize_instance()
        #self.__ladybug_npc.initilize_instance()
        self.__ladybug = None
        self.__ladybug_npc = None
        self.warWagons = []
        self.discs = []


        #self.__win = False

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
                self.discs.append(DiscGame(self.__window_size, self.__mainActions,self, "warWagon_model"))
            elif chance == 2:
                self.discs.append(DiscGame(self.__window_size, self.__mainActions,self, "rocket", (12, 28)))
            else:
                self.discs.append(DiscGame(self.__window_size, self.__mainActions,self, "flame001_model"))

    def create_warWagon(self, team):
        self.warWagons.append(WarWagon(self.__window_size, self.__mainActions, self, team))
        #self.inctances.append(WarWagon(self.__window_size, self.__mainActions, self, team))


    def click_detected(self) -> int:
        result = self.information.click_detected()
        return result


# Run the game
#game = Game()
#game.run()
