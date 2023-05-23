import pygame
from main import main
from interface import Interface
from singlePlayer import Game
from credits import Credits
from howToPlay import HowToPlay

class gameManage:
    def __init__(self):

        self.__mainActions = main()
        self.__window_size = self.__mainActions.get_window()
        self.__window, self.background = self.__start_initilzation()

        self.interface = Interface(self.__window_size,self.__mainActions)
        self.singlePlayer = Game(self.__window_size,self.__mainActions)

        self.credits = Credits(self.__window_size,self.__mainActions)
        self.howToPlay = HowToPlay(self.__window_size,self.__mainActions)
        self.currentDisplay = self.interface

        self.state = 1
        '''1 is for interface, 2 is for singleplayer, 3 is for multiplayer,
        # 4 is for how to run, 5 is for credits'''

        self.__clock = pygame.time.Clock()


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

    def __draw(self):
        self.__window.fill(self.background)
        if self.currentDisplay:
            self.currentDisplay.draw(self.__window)

        # Update the display
        pygame.display.update()

    def update(self):

        if self.state == 2:
            if self.singlePlayer is None:
                self.singlePlayer = Game(self.__window_size,self.__mainActions)
        else:
            self.singlePlayer = None

        if self.state == 1:
            self.currentDisplay = self.interface
        elif self.state == 2:
            self.currentDisplay = self.singlePlayer
            self.currentDisplay.update()
        elif self.state == 4:
            self.currentDisplay = self.howToPlay
        elif self.state == 5:
            self.currentDisplay = self.credits
        else:
            self.currentDisplay = None

    def run(self):
        framerate = 300

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Quit the game if the user closes the window
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    #if self.currentDisplay != self.singlePlayer:
                    self.state = self.currentDisplay.click_detected()
                    # if self.currentDisplay == self.interface:
                    #     self.state = self.currentDisplay.click_detected()
                    # if self.currentDisplay == self.credits:
                    #     self.state = self.currentDisplay.click_detected()

            self.update()
            self.__draw()
            self.__clock.tick(framerate)



# Run the game interface
gameManage = gameManage()
gameManage.run()
