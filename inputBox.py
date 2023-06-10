import pygame

'''input box class - in here the user enter keyboard key, and it will display it and return it to any caller object
it has different statuses and displayed and 2 more - active and inactive. the user activate the input box by clicking
on it, and deactivated it by clicking somewhere else. while active you can change the key input in it.

it gets for an input design support class "artisticDesign", location, size, fontsize and color.'''


class InputBox:
    def __init__(self, artisticDesign, x, y, width, height, font_size=32, text_color=(255, 255, 255)):
        self.__rect = pygame.Rect(x, y, width, height)
        self.__font = artisticDesign.get_default_font(font_size)

        '''colors sections, maybe soon the option to have it on input will be added. but for now - hard coded'''
        self.__active_border_color = (0, 255, 0)  # green
        self.__active_background_color = (120, 120, 120)  # dark grey

        self.__inactive_border_color = (234, 53, 53)  # pinkish red
        self.__inactive_background_color = (190, 190, 190)  # bright grey

        self.__text_color = text_color
        self.__text = ""
        self.__eve = 0
        self.__active = False
        self.__rect_border_color = self.__inactive_border_color
        self.__rect_background_color = self.__inactive_background_color

    '''activate and deactivate the box depends of the user clicked on it or elsewhere'''

    def colide(self):
        mouse_pos = pygame.mouse.get_pos()
        '''if user clicked on the box'''
        if self.__rect.collidepoint(mouse_pos):
            self.__active = True
            self.__rect_border_color = self.__active_border_color
            self.__rect_background_color = self.__active_background_color
            return True

        '''if user clicked anywhere else'''
        self.__active = False
        self.__rect_border_color = self.__inactive_border_color
        self.__rect_background_color = self.__inactive_background_color
        return False

    '''if box is activate and keyboard input is received - object will keep, display and return the last given input.'''

    def handle_event(self, event):
        if self.__active:
            self.__text = pygame.key.name(event.key)
            self.__eve = event.key
        return self.__text, self.__eve

    def draw(self, surface):
        pygame.draw.rect(surface, self.__rect_background_color, self.__rect)
        pygame.draw.rect(surface, self.__rect_border_color, self.__rect, 2)
        text_surface = self.__font.render(self.__text, True, self.__text_color)
        surface.blit(text_surface, (self.__rect.x + 5, self.__rect.y + 5))
        cursor_pos = self.__rect.x + 5 + text_surface.get_width()
        if self.__active:
            pygame.draw.line(surface, self.__text_color, (cursor_pos, self.__rect.y + 5),
                             (cursor_pos, self.__rect.y + self.__rect.height - 5))

    '''allows deactivation of the box from outer classes'''
    def disable(self):
        self.__active = False

    '''allow insertion of value from outer classes - it is used on game initialization when the setting class
    reads the current values from file, and update the input box objects accordingly.'''
    def insert_value(self, text, code):
        self.__text = text
        self.__eve = code
