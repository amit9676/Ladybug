import pygame
from typing import List
#used for def__init line in order to make the pyinstaller work, the normal list[str] wont work on compiled exe

class MessageDisplay:
    def __init__(self, size, mainActions, font_size: int, play_again_button: bool, returnState: int, lines: List[str] = None):
        self.__mainActions = mainActions
        self.__window_size = size
        self.__returnState = returnState

        # Set the font for the buttons
        self.font_text = pygame.font.SysFont('Arial', font_size)
        self.font_buttons = pygame.font.SysFont('Arial', 32)

        # Set the button position and dimensions
        button_width, button_height = 200, 50
        button_x = self.__window_size[0] // 2 - button_width // 2
        button_y = self.__window_size[1] - button_height * 2

        # Create the button
        self.back_button = pygame.Rect(button_x, button_y, button_width, button_height)
        # Set the button label
        self.back_button_label = self.font_buttons.render("Back", True, (255, 255, 255))

        self.play_again_button = None
        self.play_again_button_label = None

        if play_again_button:
            self.play_again_button = pygame.Rect(button_x, button_y, button_width, button_height)
            self.play_again_button_label = self.font_buttons.render("Play again", True, (255, 255, 255))

        self.lines = ["How to play the game:",
                      "You advance the Ladybug with the up arrow and turn it with the left and right arrow keys.","",
                      "The mission: defeat enemy Ladybug.","",
                      "It can be done with shooting fireballs as default weapon.",
                      "Aim for the target and press space to shoot it, there is infinite ammunition of it."
                      "",
                      "The second weapon is flamethrower - get close to your target and fire it by pressing 'a'."
                      , "ammunition can be gained by flamethrower discs randomly appearing on the game - ",
                      "get to them to collect them.","",
                      "The last Weapon is the rocket - also can be gained by collecting discs.",
                      "they are being automatically guided at the target, press 's' to fire them.",
                      "Both the flamethrower and rocket have limited ammunition given by every disc - use them wisely.",
                      "","There is also a support unit - the war wagon,"," summon it with the wagon Disc, and it will "
                      "assist you in the battle.","Be advised - The opponent will also seek out the discs, and you.",
                      "","ENJOY!"]
        if lines is not None:
            self.lines = lines


    def draw(self, surface):

        rendered_lines = []
        line_height = self.font_text.get_height()

        # Render the lines
        for line in self.lines:
            rendered_line = self.font_text.render(line, True, (255, 255, 255))
            rendered_lines.append(rendered_line)

        # Calculate the total height of the text
        total_text_height = len(rendered_lines) * line_height

        # Calculate the y position to center the text vertically
        y_position = self.__window_size[1] // 2 - total_text_height // 2 - 30

        # Draw the lines onto the surface
        for i, rendered_line in enumerate(rendered_lines):
            line_width = rendered_line.get_width()
            x_position = self.__window_size[0] // 2 - line_width // 2
            surface.blit(rendered_line, (x_position, y_position + i * line_height))


        # Draw the button
        y = total_text_height + y_position + 20
        if self.play_again_button is not None:
            y = self.play_again_button.y + self.back_button.height + 20

        self.back_button.y = y
        pygame.draw.rect(surface, (225, 150, 80), self.back_button)
        button_label_rect = self.back_button_label.get_rect(center=self.back_button.center)
        surface.blit(self.back_button_label, button_label_rect)

        if self.play_again_button is not None:
            self.play_again_button.y = total_text_height + y_position + 20
            pygame.draw.rect(surface, (225, 150, 80), self.play_again_button)
            button_label_rect = self.play_again_button_label.get_rect(center=self.play_again_button.center)
            surface.blit(self.play_again_button_label, button_label_rect)


        # Update the display
        pygame.display.update()

    def click_detected(self) -> int:
        mouse_pos = pygame.mouse.get_pos()
        if self.back_button.collidepoint(mouse_pos):
            return 1
        if self.play_again_button is not None:
            if self.play_again_button.collidepoint(mouse_pos):
                return 2
        return self.__returnState
