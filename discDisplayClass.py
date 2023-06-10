
from discClass import Disc
import pygame


class DiscDisplay(Disc):
    """The Disc Display Class a child class of Disc class that is used in the display section
    to show the player how much ammunition he has for each weapon...
    """
    def __init__(self, location, logicSupport, model, model_dimensions: (int, int) = (0, 0)):
        super().__init__(logicSupport, model, model_dimensions)

        self._image1 = pygame.transform.scale(self._image1, (80, 80))
        self._rect1 = self._image1.get_rect()
        self._downScale(60,model_dimensions)
        self.__initilizeDisc(location)

    def __initilizeDisc(self, location):
        self._rect1.center = location
        self._rect2.center = self._rect1.center
