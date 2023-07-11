import pygame

class Credits:
    """credit page - in here credits will be shown"""
    def __init__(self, size, logicSupport, artisticDesign):
        """initialize general data from logic and design support class"""
        self.__logicSupport = logicSupport
        self.__window_size = size
        self.__artisticDesign = artisticDesign

        '''set the necessary data for shown objects'''
        self.__font = artisticDesign.get_default_font()
        self.__image = pygame.image.load("eagle.png")
        scaling = 1.02
        new_eagle_scale = (self.__image.get_width()/scaling, self.__image.get_height()/scaling)
        self.__image = pygame.transform.scale(self.__image, new_eagle_scale)
        self.__rect = self.__image.get_rect()
        self.__rect.centerx = self.__window_size[0] / 2
        self.__rect.y = 10

        # Set the button position and dimensions
        button_width, button_height = artisticDesign.get_enlarged_button_dimensions()
        button_x = self.__window_size[0] // 2 - button_width // 2
        button_y = self.__window_size[1] - button_height * 2

        # Create the button
        self.__button = pygame.Rect(button_x, button_y, button_width, button_height)

        # Set the button label
        self.__button_label = self.__font.render("Back", True, artisticDesign.get_default_button_text_color())

    def draw(self, surface):
        # Draw the image
        surface.blit(self.__image, self.__rect)

        # Add text below the image
        text = self.__font.render("The game was developed and designed by Amit Goffer - July 2023", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.__window_size[0] // 2, self.__rect.bottom + 50))
        surface.blit(text, text_rect)

        # Draw the button
        pygame.draw.rect(surface, self.__artisticDesign.get_default_button_background_color(), self.__button)
        button_label_rect = self.__button_label.get_rect(center=self.__button.center)
        surface.blit(self.__button_label, button_label_rect)

        # Update the display
        pygame.display.update()

    def click_detected(self) -> int:
        mouse_pos = pygame.mouse.get_pos()
        if self.__button.collidepoint(mouse_pos):
            return 1
            #break
        return 6
