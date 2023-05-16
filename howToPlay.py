import pygame

class HowToPlay:
    def __init__(self, size, mainActions):
        self.__mainActions = mainActions
        self.__window_size = size

        # Set the font for the buttons
        self.font = pygame.font.SysFont('Arial', 28)

        # Set the button position and dimensions
        button_width, button_height = 200, 50
        button_x = self.__window_size[0] // 2 - button_width // 2
        button_y = self.__window_size[1] - button_height * 2

        # Create the button
        self.button = pygame.Rect(button_x, button_y, button_width, button_height)

        # Set the button label
        self.button_label = self.font.render("Back", True, (255, 255, 255))

    def draw(self, surface):
        lines = ["How to play the game:",
                 "You advance the Ladybug with the up arrow and turn it with the left and right arrow keys.","",
                 "The mission: defeat enemy Ladybug.","",
                 "It can be done with shooting fireballs as default weapon.",
                 "Aim for the target and press space to shoot it, there are infinite ammunition of it."
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

        rendered_lines = []
        line_height = self.font.get_height()

        # Render the lines
        for line in lines:
            rendered_line = self.font.render(line, True, (255, 255, 255))
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
        self.button.y = total_text_height + y_position + 20
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
