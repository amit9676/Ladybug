import pygame

class Interface:
    def __init__(self, size, mainActions):

        self.__mainActions = mainActions
        self.__window_size = size

        # Set the font for the buttons
        self.font = pygame.font.SysFont('Arial', 32)

        # Set the button positions and dimensions
        button_width, button_height = 200, 50
        button_x = self.__window_size[0] // 2 - button_width // 2
        button_y = self.__window_size[1] // 2 - button_height * 2

        # Create the buttons
        self.buttons = [
            pygame.Rect(button_x, button_y, button_width, button_height),  # Single Player
            pygame.Rect(button_x, button_y + button_height * 1.5, button_width, button_height),  # Multiplayer
            pygame.Rect(button_x, button_y + button_height * 3, button_width, button_height),  # How to Play
            pygame.Rect(button_x, button_y + button_height * 4.5, button_width, button_height)  # Credits
        ]

        # Set the button labels
        self.button_labels = [
            self.font.render("Single Player", True, (255, 255, 255)),
            self.font.render("Multiplayer", True, (255, 255, 255)),
            self.font.render("How to Play", True, (255, 255, 255)),
            self.font.render("Credits", True, (255, 255, 255))
        ]


    def draw(self, surface):

        # Draw the buttons
        for i, button in enumerate(self.buttons):
            pygame.draw.rect(surface, (225, 150, 80), button)
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
