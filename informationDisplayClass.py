import pygame


class InformationDisplayClass:
    def __init__(self, location: (int, int), window: (int,int), information: (int,int,int)):

        # Create the rectangle
        self.__rect = pygame.Rect(location[0], location[1], window[0], window[1])
        self.font = pygame.font.SysFont('Arial', 32)
        self.__hp = information[0]
        self.__flamethrower = information[1]
        self.__rockets = information[2]

    def update(self, information: (int,int,int)):
        self.__hp = information[0]
        self.__flamethrower = information[1]
        self.__rockets = information[2]

    def draw(self, surface):
        # Draw the image on the surface
        pygame.draw.rect(surface, (30, 125, 162), self.__rect)

        # Render the text
        text = self.font.render(str(self.__flamethrower), True, (255, 255, 255))

        # Calculate the position of the text
        text_rect = text.get_rect(center=self.__rect.center)

        # Draw the text on the surface
        surface.blit(text, text_rect)