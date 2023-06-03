import pygame

class Interface:
    def __init__(self, size, mainActions, artisticDesign):

        self.__mainActions = mainActions
        self.__window_size = size
        self.__artisticDesign = artisticDesign

        # Set the font for the buttons
        self.font = self.__artisticDesign.get_default_font()

        # Set the button positions and dimensions
        button_width, button_height = artisticDesign.get_enlarged_button_dimensions()
        button_x = self.__window_size[0] // 2 - button_width // 2
        button_y = self.__window_size[1] // 2 - button_height * 3

        # Create the buttons
        self.buttons = [
            pygame.Rect(button_x, button_y, button_width, button_height),  # Single Player
            pygame.Rect(button_x, button_y + button_height * 1.5, button_width, button_height),  # Multiplayer
            pygame.Rect(button_x, button_y + button_height * 3, button_width, button_height),  # How to Play
            pygame.Rect(button_x, button_y + button_height * 4.5, button_width, button_height),  # Settings
            pygame.Rect(button_x, button_y + button_height * 6, button_width, button_height)  # Credits
        ]

        # Set the button labels
        self.button_labels = [
            self.font.render("Single Player", True, self.__artisticDesign.get_default_button_text_color()),
            self.font.render("Multiplayer", True, self.__artisticDesign.get_default_button_text_color()),
            self.font.render("How to Play", True, self.__artisticDesign.get_default_button_text_color()),
            self.font.render("Settings", True, self.__artisticDesign.get_default_button_text_color()),
            self.font.render("Credits", True, self.__artisticDesign.get_default_button_text_color())
        ]


    def draw(self, surface):

        # Draw the buttons
        for i, button in enumerate(self.buttons):
            pygame.draw.rect(surface, self.__artisticDesign.get_default_button_background_color(), button)
            button_label = self.button_labels[i]
            button_label_rect = button_label.get_rect(center=button.center)
            self.__mainActions.draw(surface, button_label, button_label_rect)

        # Update the display
        pygame.display.update()



    def click_detected(self) -> int:
        mouse_pos = pygame.mouse.get_pos()
        for i, button in enumerate(self.buttons):
            if button.collidepoint(mouse_pos):
                #return self.button_clicked(i)
                return i+2
                #break
        return 1
