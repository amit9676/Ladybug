import pygame
from inputBox import InputBox


class Setting:
    def __init__(self, size, mainActions):
        self.__mainActions = mainActions
        self.__window_size = size
        self.font = pygame.font.SysFont('Arial', 32)
        self.button_size = (100, 50)

        self.wordsList = ["Advance", "Turn Right", "Turn Left", "Shoot Fireball", "Shoot Flamethrower",
                          "Shoot Rocket"]
        self.__input_boxes = []

        # Initialize input variables
        self.advance_key = ""
        self.turn_right_key = ""
        self.turn_left_key = ""
        self.shoot_fireball_key = ""
        self.shoot_flamethrower_key = ""
        self.shoot_rocket_key = ""

        self.__center_x = self.__window_size[0] // 2
        self.__center_y = self.__window_size[1] // 2
        self.__save_button = pygame.Rect(self.__center_x - self.button_size[0] - 20,
                                         self.__center_y + 175, self.button_size[0], self.button_size[1])
        self.__back_button = pygame.Rect(self.__center_x + 20, self.__center_y + 175,
                                         self.button_size[0], self.button_size[1])

        #self.inputBoxA = InputBox(x=300, y=400, width=150, height=50, font_size=34, text_color=(255, 255, 0))
        self.texts = []
        self.texts_rects = []
        self.initilize()

    def initilize(self):
        line_height = self.font.get_height()
        total_text_height = len(self.wordsList) * line_height

        # Calculate the y position to center the text vertically
        y_position = self.__window_size[1] // 2 - total_text_height // 2 - 30
        for i, item in enumerate(self.wordsList):
            self.texts.append(self.font.render(str(item) + ": ", True, (255, 255, 255)))
            self.texts_rects.append(self.texts[i].get_rect
                                    (center=(self.__center_x, y_position + i * line_height * 1.5)))
            self.__input_boxes.append(InputBox(x=self.__center_x + 240,
                                               y=y_position + i * line_height * 1.5 - 25, width=150, height=50, font_size=34,
                                               text_color=(255, 255, 0)))

    def draw(self, surface):

        for text, text_rect in zip(self.texts, self.texts_rects):
            surface.blit(text, text_rect)

        for item in self.__input_boxes:
            item.draw(surface)

        # Render the buttons
        pygame.draw.rect(surface, (225, 150, 80), self.__save_button)
        save_button_label = self.font.render("Save", True, (255, 255, 255))
        button_label_rect = save_button_label.get_rect(center=self.__save_button.center)
        surface.blit(save_button_label, button_label_rect)

        pygame.draw.rect(surface, (225, 150, 80), self.__back_button)
        back_button_label = self.font.render("Back", True, (255, 255, 255))
        button_label_rect = back_button_label.get_rect(center=self.__back_button.center)
        surface.blit(back_button_label, button_label_rect)

        #self.inputBoxA.draw(surface)

    def update(self, event):
        for item in self.__input_boxes:
            item.handle_event(event)
        #self.inputBoxA.handle_event(event)

    def click_detected(self):
        mouse_pos = pygame.mouse.get_pos()
        activated_input_box = False
        for item in self.__input_boxes:
            if not item.colide():
                item.disable()
            else:
                activated_input_box = True

        if self.__save_button.collidepoint(mouse_pos):
            # Perform save operation here
            return 1
        elif self.__back_button.collidepoint(mouse_pos):
            return 1
        elif activated_input_box:
            return 5

        return 5
