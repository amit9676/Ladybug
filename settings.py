import pygame
from inputBox import InputBox


class Setting:
    def __init__(self, size, mainActions, artisticDesign):
        self.__mainActions = mainActions
        self.__window_size = size
        self.__artisticDesign = artisticDesign
        self.font = artisticDesign.get_default_font()
        self.button_size = artisticDesign.get_default_button_dimensions()

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
        self.current_keys = []
        self.initilize()

        self.doubleKeyNote = "two or more of options have the same keyboard key, please change it"
        self.doubleKeyNoteActive = False
        self.blankKeyNote = "one or more key input box is blank, please set a key for it"
        self.blankKeyNoteActive = False

        self.disabled_save_background_color = (236, 188, 145)
        self.disabled_save_text_color = (220,220,220)
        self.disable_save_button = False

        self.original_save_background_color = artisticDesign.get_default_button_background_color()
        self.original_save_text_color = artisticDesign.get_default_button_text_color()

        self.save_background_color = self.original_save_background_color
        self.save_text_color = self.original_save_text_color
        self.update(None)

    def initilize(self):
        line_height = self.font.get_height()
        total_text_height = len(self.wordsList) * line_height

        # Calculate the y position to center the text vertically
        y_position = self.__window_size[1] // 2 - total_text_height // 2 - 30
        for i, item in enumerate(self.wordsList):
            self.texts.append(self.font.render(str(item) + ": ", True, self.__artisticDesign.get_default_button_text_color()))
            self.texts_rects.append(self.texts[i].get_rect
                                    (center=(self.__center_x, y_position + i * line_height * 1.5)))
            self.__input_boxes.append(InputBox(artisticDesign=self.__artisticDesign,x=self.__center_x + 240,
                                               y=y_position + i * line_height * 1.5 - 25, width=150, height=50, font_size=34,
                                               text_color=(255, 255, 0)))
            #self.current_keys.append("")
        self.current_keys = self.readFromFile()
        for i, item in enumerate(self.__input_boxes):
            item.insert_value(self.current_keys[i])
        #print(self.current_keys)

    def draw(self, surface):

        for text, text_rect in zip(self.texts, self.texts_rects):
            surface.blit(text, text_rect)

        for item in self.__input_boxes:
            item.draw(surface)

        # Render the buttons
        pygame.draw.rect(surface, self.save_background_color, self.__save_button)
        save_button_label = self.font.render("Save", True, self.save_text_color)
        button_label_rect = save_button_label.get_rect(center=self.__save_button.center)
        surface.blit(save_button_label, button_label_rect)

        pygame.draw.rect(surface, self.__artisticDesign.get_default_button_background_color(), self.__back_button)
        back_button_label = self.font.render("Back", True, self.__artisticDesign.get_default_button_text_color())
        button_label_rect = back_button_label.get_rect(center=self.__back_button.center)
        surface.blit(back_button_label, button_label_rect)

        smaller_font = self.__artisticDesign.get_default_font(17)
        # Draw doubleKeyNote below the save button
        double_key_note_text = smaller_font.render(self.doubleKeyNote, True, self.__artisticDesign.get_default_button_text_color())
        double_key_note_rect = double_key_note_text.get_rect(center=(self.__center_x, self.__save_button.bottom + 20))
        if self.doubleKeyNoteActive:
            surface.blit(double_key_note_text, double_key_note_rect)

        # Draw blankKeyNote below the save button and doubleKeyNote
        blank_key_note_text = smaller_font.render(self.blankKeyNote, True,self.__artisticDesign.get_default_button_text_color())
        blank_key_note_rect = blank_key_note_text.get_rect(center=(self.__center_x, double_key_note_rect.bottom + 20))
        if self.blankKeyNoteActive:
            surface.blit(blank_key_note_text, blank_key_note_rect)


    def update(self, event):
        #print(self.current_keys)
        for i, item in enumerate(self.__input_boxes):
            if event is not None:
                self.current_keys[i] = item.handle_event(event)

        self.blankKeyNoteActive = self.checkBlankKey()
        self.doubleKeyNoteActive = self.checkDoubleKey()
        if self.blankKeyNoteActive or self.doubleKeyNoteActive:
            self.disable_save_button = True
            self.save_text_color = self.disabled_save_text_color
            self.save_background_color = self.disabled_save_background_color
        else:
            self.disable_save_button = False
            self.save_text_color = self.original_save_text_color
            self.save_background_color = self.original_save_background_color
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
            if not self.disable_save_button:
                self.printToFile()
                return 1
            # for item in self.current_keys:
            #     print(item)
            return 5
        elif self.__back_button.collidepoint(mouse_pos):
            return 1
        elif activated_input_box:
            return 5

        return 5

    def checkBlankKey(self) -> bool:
        for item in self.current_keys:
            if item == "":
                return True
        return False

    def checkDoubleKey(self) -> bool:
        lst = self.current_keys
        for i in range(len(lst) - 1):
            for j in range(i + 1, len(lst)):
                if lst[i] == lst[j] and lst[i] != "":
                    return True
        return False

    def printToFile(self):
        with open("keys.txt", "w") as file:
            file.write("**** DO NOT CHANGE THIS FILE!!!!!!****\n")
            file.write("keys:\n")

            for i in range(len(self.wordsList)):
                line = f"{self.wordsList[i]} = {self.current_keys[i]}\n"
                file.write(line)

    def readFromFile(self):
        settings = []

        with open("keys.txt", 'r') as file:
            lines = file.readlines()

            # Skip the first line (header)
            for line in lines[2:]:
                line = line.strip()  # Remove leading/trailing whitespaces
                if line:
                    key, value = line.split(' = ')
                    settings.append(value)

        return settings
