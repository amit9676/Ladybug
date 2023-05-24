import pygame


class InputBox:
    def __init__(self, x, y, width, height, font_size=32, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.SysFont('Arial', font_size)


        '''colors sections, maybe soon the option to have it on input will be added. but for now - hard coded'''
        self.active_border_color = (0, 255, 0) #green
        self.active_background_color = (120,120,120) #dark grey

        self.inactive_border_color = (234, 53, 53) #pinkish red
        self.inactive_background_color = (190,190,190) #bright grey

        self.text_color = text_color
        self.text = ""
        self.active = False
        self.rect_border_color = self.inactive_border_color
        self.rect_background_color = self.inactive_background_color

    def colide(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.active = True
            self.rect_border_color = self.active_border_color
            self.rect_background_color = self.active_background_color
            return True
            # break
        self.active = False
        self.rect_border_color = self.inactive_border_color
        self.rect_background_color = self.inactive_background_color
        return False

    def handle_event(self, event):
        if self.active:
            self.text = pygame.key.name(event.key)

    def draw(self, surface):
        #pygame.draw.rect(surface, self.rect_color, self.rect, 2)

        #pygame.draw.rect(surface, self.rect_color, self.rect, 2)
        pygame.draw.rect(surface, self.rect_background_color, self.rect)
        pygame.draw.rect(surface, self.rect_border_color, self.rect, 2)
        text_surface = self.font.render(self.text, True, self.text_color)
        surface.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))
        cursor_pos = self.rect.x + 5 + text_surface.get_width()
        if self.active:
            pygame.draw.line(surface, self.text_color, (cursor_pos, self.rect.y + 5),
                             (cursor_pos, self.rect.y + self.rect.height - 5))

    def disable(self):
        self.active = False

