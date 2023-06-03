import pygame

'''this class is a support class - it holds all the size and color for buttons/background and such for easy design
implementation through the game interface'''


class ArtisticDesignClass:
    def __init__(self):
        pass

    def get_default_button_text_color(self) -> (int, int, int):
        return (255, 255, 255) # white

    def get_default_button_background_color(self) -> (int, int, int):
        return (225, 150, 80) # orange

    def get_default_font(self, val=32, font='Arial'):
        return pygame.font.SysFont(font, val)

    def get_default_button_dimensions(self) -> (int,int):
        #return (width, height)
        return 100,50

    def get_enlarged_button_dimensions(self) -> (int,int):
        #return (width, height)
        return 200,50
