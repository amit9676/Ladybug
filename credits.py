import pygame

class Credits:
    def __init__(self, size, mainActions):
        self.__mainActions = mainActions
        self.__window_size = size

        # Set the font for the buttons
        self.font = pygame.font.SysFont('Arial', 32)
        self.__image = pygame.image.load("eagle.png")
        scaling = 1.02
        new_eagle_scale = (self.__image.get_width()/scaling, self.__image.get_height()/scaling)
        self.__image = pygame.transform.scale(self.__image, new_eagle_scale)
        self.__rect = self.__image.get_rect()
        self.__rect.centerx = self.__window_size[0] / 2
        self.__rect.y = 10

        # Set the button position and dimensions
        button_width, button_height = 200, 50
        button_x = self.__window_size[0] // 2 - button_width // 2
        button_y = self.__window_size[1] - button_height * 2

        # Create the button
        self.button = pygame.Rect(button_x, button_y, button_width, button_height)

        # Set the button label
        self.button_label = self.font.render("Back", True, (255, 255, 255))

    def draw(self, surface):
        # Draw the image
        surface.blit(self.__image, self.__rect)

        # Add text below the image
        text = self.font.render("The game was developed and designed by Amit Goffer - June 2023", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.__window_size[0] // 2, self.__rect.bottom + 50))
        surface.blit(text, text_rect)

        # Draw the button
        pygame.draw.rect(surface, (225, 150, 80), self.button)
        button_label_rect = self.button_label.get_rect(center=self.button.center)
        surface.blit(self.button_label, button_label_rect)

        # Update the display
        pygame.display.update()

    def click_detected(self) -> int:
        mouse_pos = pygame.mouse.get_pos()
        if self.button.collidepoint(mouse_pos):
            #return self.button_clicked(i)
            return 1
            #break
        return 5
