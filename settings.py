import pygame
from inputBox import InputBox

'''the setting class is used for the user to be able to change game keys - on initialization it reads the current keys
from keys.txt file - and passed them to inputbox objects to display.
setting class contain various input box - one for each game action (move, shoot, turn), and without the user is able
to decide which keyboard key will trigget the action.'''


class Setting:
    def __init__(self, size, artisticDesign):
        self.__window_size = size
        self.__artisticDesign = artisticDesign
        self.__font = artisticDesign.get_default_font()
        self.__button_size = artisticDesign.get_default_button_dimensions()

        self.__wordsList = ["Advance", "Turn Right", "Turn Left", "Shoot Fireball", "Shoot Flamethrower",
                            "Shoot Rocket"]
        self.__input_boxes = []

        self.__center_x = self.__window_size[0] // 2
        self.__center_y = self.__window_size[1] // 2
        self.__save_button = pygame.Rect(self.__center_x - self.__button_size[0] - 20,
                                         self.__center_y + 175, self.__button_size[0], self.__button_size[1])
        self.__back_button = pygame.Rect(self.__center_x + 20, self.__center_y + 175,
                                         self.__button_size[0], self.__button_size[1])

        '''text list fields initialization'''
        self.__texts = []
        self.__texts_rects = []
        self.__current_keys = []

        self.__initilize()  # initilize the input boxes and texts

        '''some nots about possible saving requirements'''
        self.__doubleKeyNote = "two or more of options have the same keyboard key, please change it"
        self.__doubleKeyNoteActive = False
        self.__blankKeyNote = "one or more key input box is blank, please set a key for it"
        self.__blankKeyNoteActive = False

        '''disabled save button properties'''
        self.__disabled_save_background_color = (236, 188, 145)
        self.__disabled_save_text_color = (220, 220, 220)
        self.__disable_save_button = False

        '''enabled save button properties'''
        self.__original_save_background_color = artisticDesign.get_default_button_background_color()
        self.__original_save_text_color = artisticDesign.get_default_button_text_color()

        '''actual used save button properties'''
        self.__save_background_color = self.__original_save_background_color
        self.__save_text_color = self.__original_save_text_color

        '''initial object update (with no keyboard input), used to update the input boxes with the initial file
        extracted values'''
        self.update(None)

    '''initialize positions and values for buttons, text and input boxes'''

    def __initilize(self):
        line_height = self.__font.get_height()
        total_text_height = len(self.__wordsList) * line_height

        # Calculate the y position to center the text vertically
        y_position = self.__window_size[1] // 2 - total_text_height // 2 - 30
        for i, item in enumerate(self.__wordsList):
            self.__texts.append(self.__font.render(str(item) + ": ", True,
                                                   self.__artisticDesign.get_default_button_text_color()))
            self.__texts_rects.append(self.__texts[i].get_rect
                                      (center=(self.__center_x, y_position + i * line_height * 1.5)))
            self.__input_boxes.append(InputBox(artisticDesign=self.__artisticDesign, x=self.__center_x + 240,
                                               y=y_position + i * line_height * 1.5 - 25, width=150, height=50,
                                               font_size=34,
                                               text_color=(255, 255, 0)))

        self.__current_keys = self.readFromFile()  # read initial values from file
        '''insert to each input box the inital extracted from the file'''
        for i, item in enumerate(self.__input_boxes):
            item.insert_value(self.__current_keys[i])

    def draw(self, surface):
        for text, text_rect in zip(self.__texts, self.__texts_rects):
            surface.blit(text, text_rect)

        for item in self.__input_boxes:
            item.draw(surface)

        # Render the buttons
        pygame.draw.rect(surface, self.__save_background_color, self.__save_button)
        save_button_label = self.__font.render("Save", True, self.__save_text_color)
        button_label_rect = save_button_label.get_rect(center=self.__save_button.center)
        surface.blit(save_button_label, button_label_rect)

        pygame.draw.rect(surface, self.__artisticDesign.get_default_button_background_color(), self.__back_button)
        back_button_label = self.__font.render("Back", True, self.__artisticDesign.get_default_button_text_color())
        button_label_rect = back_button_label.get_rect(center=self.__back_button.center)
        surface.blit(back_button_label, button_label_rect)

        smaller_font = self.__artisticDesign.get_default_font(17)
        # Draw doubleKeyNote below the save button
        double_key_note_text = smaller_font.render(self.__doubleKeyNote, True,
                                                   self.__artisticDesign.get_default_button_text_color())
        double_key_note_rect = double_key_note_text.get_rect(center=(self.__center_x, self.__save_button.bottom + 20))
        if self.__doubleKeyNoteActive:
            surface.blit(double_key_note_text, double_key_note_rect)

        # Draw blankKeyNote below the save button and doubleKeyNote
        blank_key_note_text = smaller_font.render(self.__blankKeyNote, True,
                                                  self.__artisticDesign.get_default_button_text_color())
        blank_key_note_rect = blank_key_note_text.get_rect(center=(self.__center_x, double_key_note_rect.bottom + 20))
        if self.__blankKeyNoteActive:
            surface.blit(blank_key_note_text, blank_key_note_rect)

    '''update the save button status based on coming keyboard input'''

    def update(self, event):
        '''update the current keys from input boxes'''
        for i, item in enumerate(self.__input_boxes):
            if event is not None:
                self.__current_keys[i] = item.handle_event(event)

        '''update the save button properties according to the new developments.
        if any key is blank (which should be occured, but safe guard exists nonetheless), or if the same key is used
        for two or more actions - saving the settings will not be possible, only different, valid keyboard is allowed
        for each action.'''
        self.__blankKeyNoteActive = self.__checkBlankKey()
        self.__doubleKeyNoteActive = self.__checkDoubleKey()
        if self.__blankKeyNoteActive or self.__doubleKeyNoteActive:
            self.__disable_save_button = True
            self.__save_text_color = self.__disabled_save_text_color
            self.__save_background_color = self.__disabled_save_background_color
        else:
            self.__disable_save_button = False
            self.__save_text_color = self.__original_save_text_color
            self.__save_background_color = self.__original_save_background_color

    '''use click handler function'''

    def click_detected(self):
        mouse_pos = pygame.mouse.get_pos()
        activated_input_box = False
        for item in self.__input_boxes:
            if not item.colide():
                item.disable()
            else:
                activated_input_box = True

        if self.__save_button.collidepoint(mouse_pos):
            '''saving is allowed only when all requirements are met (no dual, no blank)'''
            if not self.__disable_save_button:
                self.__writeToFile()
                return 1
            return 5
        elif self.__back_button.collidepoint(mouse_pos):
            return 1
        elif activated_input_box:
            return 5

        return 5

    '''this function determines if one or more input boxes does not has any value'''

    def __checkBlankKey(self) -> bool:
        for item in self.__current_keys:
            if item == "":
                return True
        return False

    '''this functions determine if two (or more) input boxes contain the same (valid) value.'''

    def __checkDoubleKey(self) -> bool:
        lst = self.__current_keys
        for i in range(len(lst) - 1):
            for j in range(i + 1, len(lst)):
                if lst[i] == lst[j] and lst[i] != "":
                    return True
        return False

    '''this function writes to keys.txt the saved keys for each action. thus the playing keys are updates'''

    def __writeToFile(self):
        with open("keys.txt", "w") as file:
            file.write("**** DO NOT CHANGE THIS FILE!!!!!!****\n")
            file.write("keys:\n")

            for i in range(len(self.__wordsList)):
                line = f"{self.__wordsList[i]} = {self.__current_keys[i]}\n"
                file.write(line)

    '''this function reads from the file the current keys, used on initialization, for now it remains public as
    it should be used on game initialization to get the playing keys. it might move to "main" class
    (or future name - logicSupport)'''

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
