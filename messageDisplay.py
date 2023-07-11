import pygame
from typing import List
#used for def__init line in order to make the pyinstaller work, the normal list[str] wont work on compiled exe

'''this class is used to display a message in the screen, the howtoplay message is chosen as default due to its length.
however it is possible to enter custum input to override it.'''
class MessageDisplay:
    def __init__(self, size, logicSupport, artisticDesign, font_size: int, play_again_button: bool, returnState: int, lines: List[str] = None):
        self.__logicSupport = logicSupport
        self.__window_size = size
        self.__returnState = returnState
        self.__artisticDesign = artisticDesign

        # Set the font for the buttons
        self.__font_text = artisticDesign.get_default_font(font_size)
        self.__font_buttons = artisticDesign.get_default_font()

        # Set the button position and dimensions
        button_width, button_height = artisticDesign.get_enlarged_button_dimensions()
        button_x = self.__window_size[0] // 2 - button_width // 2
        button_y = self.__window_size[1] - button_height * 2

        # Create the button
        self.__back_button = pygame.Rect(button_x, button_y, button_width, button_height)
        # Set the button label
        self.__back_button_label = self.__font_buttons.render("Back", True, artisticDesign.get_default_button_text_color())

        self.__play_again_button = None
        self.__play_again_button_label = None

        if play_again_button:
            self.__play_again_button = pygame.Rect(button_x, button_y, button_width, button_height)
            self.__play_again_button_label = self.__font_buttons.render("Play again", True, artisticDesign.get_default_button_text_color())

        self.__lines = ["How to play the game:",
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
                      "","There is also a support unit - the war wagon."," summon it with the wagon Disc, and it will "
                      "assist you in the battle.","Be advised - The opponent will also seek out the discs, and you.",
                      "",
                      "in settings you may change the game keys to any keys that you wish.",
                      "it will be saved for that moment on.",
                      "","ENJOY!"]
        if lines is not None:
            self.__lines = lines


    def draw(self, surface):

        rendered_lines = []
        line_height = self.__font_text.get_height()

        # Render the lines
        for line in self.__lines:
            rendered_line = self.__font_text.render(line, True, self.__artisticDesign.get_default_button_text_color())
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
        if self.__play_again_button is not None:
            y = self.__play_again_button.y + self.__back_button.height + 20

        self.__back_button.y = y
        pygame.draw.rect(surface, self.__artisticDesign.get_default_button_background_color(), self.__back_button)
        button_label_rect = self.__back_button_label.get_rect(center=self.__back_button.center)
        surface.blit(self.__back_button_label, button_label_rect)

        if self.__play_again_button is not None:
            self.__play_again_button.y = total_text_height + y_position + 20
            pygame.draw.rect(surface, self.__artisticDesign.get_default_button_background_color(), self.__play_again_button)
            button_label_rect = self.__play_again_button_label.get_rect(center=self.__play_again_button.center)
            surface.blit(self.__play_again_button_label, button_label_rect)


        # Update the display
        pygame.display.update()

    '''click interaction class - reacts to use clicks, if its on any button - it reacts accordingly'''
    def click_detected(self) -> int:
        mouse_pos = pygame.mouse.get_pos()
        if self.__back_button.collidepoint(mouse_pos):
            return 1
        if self.__play_again_button is not None:
            if self.__play_again_button.collidepoint(mouse_pos):
                return 2
        return self.__returnState
