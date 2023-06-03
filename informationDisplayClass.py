import pygame
from discDisplayClass import DiscDisplay

'''this class is the information display class - it displays in real time the condition of player hp and ammunition.
it is activated during the game, and placed on the bottom of it - it gets the location and constant
 information from the game class.'''
class InformationDisplayClass:
    def __init__(self, location: (int, int), mainActions, window: (int,int),
                 information: (int,int,int), artisticDesign):

        '''get logic and design support classes'''
        self.__mainActions = mainActions
        self.__artisticDesign = artisticDesign

        # Create the rectangle
        self.__rect = pygame.Rect(location[0], location[1], window[0], window[1])
        self.font = self.__artisticDesign.get_default_font()

        '''set the variables which will be display'''
        self.__hp = information[0]
        self.__flamethrower = information[1]
        self.__rockets = information[2]

        '''set the display discs which will be displayed with the data'''
        self.__displayHeartDisc = DiscDisplay((location[0] + 50, location[1] + 20), self.__mainActions, "heart", (40, 40))
        self.__displayFlameDisc = DiscDisplay(location, self.__mainActions, "flame001_model")
        self.__displayRocketDisc = DiscDisplay(location, self.__mainActions, "rocket", (12, 28))

        # Calculate the horizontal spacing between the display objects
        object_spacing = self.__rect.width // 5

        # Calculate the vertical center of the rectangle
        vertical_center = self.__rect.centery

        # Calculate the positions of the display objects
        self.__display_heart_pos = (self.__rect.left + object_spacing, vertical_center)
        self.__display_flame_pos = (self.__rect.left + (2*object_spacing), vertical_center)
        self.__display_rocket_pos = (self.__rect.left +(3 * object_spacing), vertical_center)

        # Create the display objects
        self.__displayHeartDisc = DiscDisplay(self.__display_heart_pos, self.__mainActions, "heart", (40, 40))
        self.__displayFlameDisc = DiscDisplay(self.__display_flame_pos, self.__mainActions, "flame001_model")
        self.__displayRocketDisc = DiscDisplay(self.__display_rocket_pos, self.__mainActions, "rocket", (24, 48))

        # Create the button
        button_width, button_height = artisticDesign.get_default_button_dimensions()
        button_x = self.__rect.left +(4 * object_spacing)
        button_y = vertical_center - (button_height / 2)

        self.__button = pygame.Rect(button_x, button_y, button_width, button_height)

        # Set the button label
        self.__button_label = self.font.render("Back", True, self.__artisticDesign.get_default_button_text_color())

    '''update the screen variables - the method gets the required info from the game object, and updates it.'''
    def update(self, information: (int,int,int)):
        self.__hp = information[0]
        self.__flamethrower = information[1]
        self.__rockets = information[2]

    def draw(self, surface):
        # Draw the image on the surface
        pygame.draw.rect(surface, (30, 125, 162), self.__rect)

        # Render the text
        hp_text = self.font.render(" x " + str(self.__hp), True, self.__artisticDesign.get_default_button_text_color())
        flame_text = self.font.render(" x " + str(self.__flamethrower), True, self.__artisticDesign.get_default_button_text_color())
        rockets_text = self.font.render(" x " + str(self.__rockets), True, self.__artisticDesign.get_default_button_text_color())

        '''draw the discs with its own class draw function.'''
        self.__displayHeartDisc.draw(surface)
        self.__displayFlameDisc.draw(surface)
        self.__displayRocketDisc.draw(surface)

        # Calculate the position of the text
        hp_text_rect = hp_text.get_rect(
            center=(self.__display_heart_pos[0] + self.__displayHeartDisc.get_dimensions()[0],
                    self.__display_heart_pos[1]))

        flame_text_rect = flame_text.get_rect(
            center=(self.__display_flame_pos[0] + self.__displayFlameDisc.get_dimensions()[0],
                    self.__display_flame_pos[1]))

        rockets_text_rect = rockets_text.get_rect(
            center=(self.__display_rocket_pos[0] + self.__displayRocketDisc.get_dimensions()[0],
                    self.__display_rocket_pos[1]))

        pygame.draw.rect(surface, self.__artisticDesign.get_default_button_background_color(), self.__button)
        button_label_rect = self.__button_label.get_rect(center=self.__button.center)


        # Draw the text on the surface
        surface.blit(hp_text, hp_text_rect)
        surface.blit(flame_text, flame_text_rect)
        surface.blit(rockets_text, rockets_text_rect)
        surface.blit(self.__button_label, button_label_rect)

    '''the object has a button - this method is being invoked by outer function which pick up user clicks - it 
    read current cursor position - if its over the back button - it means the player clicked the back button and the
    game will end and the user will return to menu screen. else - nothing happened.'''
    def click_detected(self) -> int:
        mouse_pos = pygame.mouse.get_pos()
        if self.__button.collidepoint(mouse_pos):
            return 1
            #break
        return 2