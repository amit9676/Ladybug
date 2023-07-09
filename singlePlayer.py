import pygame
import random
from ladybugPlayerClass import Ladybug_Player
from flagClass import Flag
from warWagonClass import WarWagon
from ladybugNPCClass import Ladybug_NPC
from discGameClass import DiscGame
from informationDisplayClass import InformationDisplayClass
from logicSupportClass import LogicSupportClass

'''Single player class - holds all data that related to the game, manages it and updates it. in contant with all various
game units, projectile and ect to get current game data.'''

class Game:
    def __init__(self, size, logicSupport, artisticDesign, keys):
        # Create the ladybug and flag objects
        self.__logicSupport = logicSupport
        self.__artisticDesign = artisticDesign
        # self.__window_size = size
        information_height_size = 100
        self.__window_size = (size[0], size[1] - information_height_size)
        self.__ladybug = Ladybug_Player(window=self.__window_size, logicSupport=self.__logicSupport, game=self,
                                        team="red", keys=keys)
        self.__ladybug_npc = Ladybug_NPC(self.__window_size, self.__logicSupport, self, "blue")
        self.__information = InformationDisplayClass((0, self.__window_size[1]), self.__logicSupport
                                                     , (self.__window_size[0], information_height_size),
                                                     self.__ladybug.get_ladybug_data(), artisticDesign)

        # a list of all inctances (ladybugs, warwagons and future instances)
        self.__ladybugs = []
        self.__warWagons = []
        self.__discs = []

        '''the placement of the following 2 line of codes is TEMPORARY for testing'''
        self.__ladybugs.append(self.__ladybug)
        self.__ladybugs.append(self.__ladybug_npc)
        ''' until here'''

        # Set the game state to "running"
        self.__running = True
        self.__clock = pygame.time.Clock()
        self.__playing = True
        self.__win = False

    def get_window_size(self) -> (int, int):
        return self.__window_size

    '''this method compiles a list of all actives instances on the game - that include player controlled ladybugs,
    NPC ladybugs, war wagon and future instances. this method has to be PUBLIC in order for the "players" to receive
    real time data about other players - instances, and their current location. all inctances must have a public method
    "get_current_location()" in order for every instance to "read the map"'''

    def get_inctances(self):
        return self.__ladybugs

    def get_wagons(self):
        return self.__warWagons

    '''update the game - in here make sure everything in the game is being updated.'''

    def update(self) -> int:

        # Update the ladybug object
        keys = pygame.key.get_pressed()
        self.__ladybug.update(keys)
        self.__ladybug_npc.update()
        self.__information.update(self.__ladybug.get_ladybug_data())

        '''war wagons'''
        for w in self.__warWagons:
            w.update()
            if w.self_destruct and not w.fireballs:
                self.__warWagons.remove(w)

        '''discs'''
        self.create_disk()
        for d in self.__discs:
            d.update()
            if d.self_destruct:
                self.__discs.remove(d)

        '''check for collision between warwagons and ladybug'''
        self.__collision_ladybug_warwagon()
        self.__collision_ladybug_disc()
        self.__collision_warwagons_disc()

        if self.__ladybug.get_hitpoints() <= 0:
            return -1
        elif self.__ladybug_npc.get_hitpoints() <= 0:
            return 1
        return 0

    '''main draw method - in here make sure every game instance is being drown'''

    def draw(self, window):

        for d in self.__discs:
            d.draw(window)


        # Draw the ladybug and on the window
        self.__ladybug.draw(window)

        self.__ladybug_npc.draw(window)

        '''draw war wagon and its projectiles'''
        for w in self.__warWagons:
            w.draw(window)
            for fireball in w.fireballs:
                fireball.draw(window)



        '''draw all projectiles'''
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
        '''end of projectile drawing'''

        self.__information.draw(window)

    def create_disk(self):
        """default value 7500
        this method is responsible to create a disk at probablity of 1 to 7500.
        currently - there are 3 types of disk:
        war wagon - which summons war wagon to help the summoner.
        rockets ammo, and flamethrower ammo."""
        probability = 750
        chance = random.randint(1, probability)
        # location = self.__mainActions.generate_random_location(self.__window_size)
        if chance % probability == 0:
            chance = random.randint(1, 3)
            if chance == 1:
                self.__discs.append(DiscGame(self.__window_size, self.__logicSupport, self, "warWagon_model"))
            elif chance == 2:
                self.__discs.append(DiscGame(self.__window_size, self.__logicSupport, self, "rocket", (12, 28)))
            else:
                self.__discs.append(DiscGame(self.__window_size, self.__logicSupport, self, "flame001_model"))

    def create_warWagon(self, team):
        self.__warWagons.append(WarWagon(window=self.__window_size, logicSupport=self.__logicSupport, game=self, team=team))

    '''this method is used to check collisions between war wagons and ladybugs.
    if there is a collision - the ladybug hit will lose hp for every frame of collision REGARDLESS of teams'''
    def __collision_ladybug_warwagon(self):
        for l in self.__ladybugs:
            if self.__logicSupport.impact_identifier(l,None, self.__warWagons):
                l.decrease_hitPoints(1)

    def __collision_ladybug_disc(self):
        for d in self.__discs:
            impacted = self.__logicSupport.impact_identifier(d,None, self.__ladybugs)
            if impacted:
                if d.get_model() == "warWagon_model":
                    self.create_warWagon(impacted[0].get_instance_struct().get_team())
                elif d.get_model() == "rocket":
                    impacted[0].add_rockets()
                elif d.get_model() == "flame001_model":
                    impacted[0].add_flamethrower()
                d.self_destruct = True

    def __collision_warwagons_disc(self):
        for d in self.__discs:
            impacted = self.__logicSupport.impact_identifier(d,None, self.__warWagons)
            if impacted:
                if d.get_model() == "warWagon_model":
                    self.create_warWagon(impacted[0].get_instance_struct().get_team())
                d.self_destruct = True


    '''if user click on back button in information object, so data passes through this class from/to
     gameManage-information display'''
    def click_detected(self) -> int:
        result = self.__information.click_detected()
        return result
