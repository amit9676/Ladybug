import pygame
from logicSupportClass import LogicSupportClass
from interface import Interface
from singlePlayer import Game
from credits import Credits
from messageDisplay import MessageDisplay
from settings import Setting
from artisticDesignClass import ArtisticDesignClass
from fileHandlerClass import FileHandler

'''main game class - this class initilize the entire program which is the Ladybug game
this class consists of objects of all possible options, and management system to handle them.'''


class gameManage:
    def __init__(self):

        self.__logicSupport = LogicSupportClass()
        self.__window_size = self.__logicSupport.get_window()
        self.__window, self.background = self.__start_initilzation()
        self.__artisticDesign = ArtisticDesignClass()
        self.__fileHandler = FileHandler()
        self.__keys = self.__fileHandler.readFromFile()
        #print(keys)

        '''initlize the different game components such as interface, game, credits, settings and instructions.'''
        self.__interface = Interface(self.__window_size, self.__logicSupport, self.__artisticDesign)
        self.__singlePlayer = Game(self.__window_size, self.__logicSupport, self.__artisticDesign, self.__keys)

        self.__credits = Credits(self.__window_size, self.__logicSupport, self.__artisticDesign)

        self.__howToPlay = self.__generate_message_display_window(26, False, 4)
        self.__settings = Setting(self.__window_size, self.__artisticDesign, self.__fileHandler)

        self.__lost = self.__generate_message_display_window(45,True,7,"YOU LOSE")
        self.__win = self.__generate_message_display_window(45,True,8,"YOU WIN")

        self.__currentDisplay = self.__interface

        self.__state = 1
        '''1 is for interface, 2 is for singleplayer, 3 is for multiplayer,
        # 4 is for how to run, 5 is for settings, 6 is for credits, 7 is for lose, 8 is for win'''

        self.__clock = pygame.time.Clock()

    def __start_initilzation(self):
        pygame.init()

        # Create the window
        window = pygame.display.set_mode((self.__window_size[0], self.__window_size[1]))
        pygame.display.set_caption("Ladybug")
        pygame_icon = pygame.image.load('images/ladybug_red.png')
        pygame.display.set_icon(pygame_icon)

        # Set the background color
        background_color = (135, 206, 235)
        return window, background_color

    def __draw(self):
        self.__window.fill(self.background)
        if self.__currentDisplay:
            self.__currentDisplay.draw(self.__window)

        # Update the display
        pygame.display.update()

    '''update the different component of the game depend on the situation of the game
    the variable state is being constantly updated by the run method, and the update knows to update
    the game interface accordingly.'''
    def __update(self):

        if self.__state == 2:
            if self.__singlePlayer is None:
                self.__keys = self.__fileHandler.readFromFile()
                self.__singlePlayer = Game(self.__window_size, self.__logicSupport, self.__artisticDesign, self.__keys)
        else:
            self.__singlePlayer = None


        if self.__state == 1:
            self.__currentDisplay = self.__interface
        elif self.__state == 2:
            self.__currentDisplay = self.__singlePlayer
            result = self.__currentDisplay.update()
            if result == -1:
                self.__state = 7
            elif result == 1:
                self.__state = 8
        elif self.__state == 4:
            self.__currentDisplay = self.__howToPlay
        elif self.__state == 5:
            self.__currentDisplay = self.__settings
            # self.currentDisplay.update()
        elif self.__state == 6:
            self.__currentDisplay = self.__credits
        elif self.__state == 7:
            self.__currentDisplay = self.__lost
        elif self.__state == 8:
            self.__currentDisplay = self.__win
        else:
            self.__currentDisplay = None

    '''set the framerate and handle user mouse and keyboard input - the run method is the main game loop - in the loop
    it takes care of event, and passes it to the different objects and methods accordingly.
    
    the main game loop also constantly updates the game, draw it and updates the clock.
    the game framerate is set to 300 - that in order to allow ladybug to rotate at degree of 1 angle with reasonable
    speed.'''
    def run(self):
        framerate = 300

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Quit the game if the user closes the window
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.__state = self.__currentDisplay.click_detected()

                elif event.type == pygame.KEYDOWN:
                    if self.__currentDisplay == self.__settings:
                        self.__settings.update(event)

            self.__update()
            self.__draw()
            self.__clock.tick(framerate)

    '''method to generate message display object with more ease - just enter the parameters and message display object
    will be returned.'''
    def __generate_message_display_window(self, font_size: int, play_again_button: bool,
                                          return_state: int, message=None)-> MessageDisplay:
        if message is None:
            return MessageDisplay(size=self.__window_size, logicSupport=self.__logicSupport,
                                  artisticDesign=self.__artisticDesign, font_size=font_size, play_again_button=play_again_button,
                                  returnState=return_state)
        return MessageDisplay(size=self.__window_size, logicSupport=self.__logicSupport,
                              artisticDesign=self.__artisticDesign, font_size=font_size, play_again_button=play_again_button,
                              returnState=return_state, lines=[message])


# Run the game interface
gameManage = gameManage()
gameManage.run()
