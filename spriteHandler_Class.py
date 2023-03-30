import pygame

'''this classed handles Sprites - it takes sprite and makes it an animation'''


class Sprite:
    """initialization method - it takes the filename, width and height of each frame, amount of rows and
    columns, and frame rate"""

    def __init__(self, filename, frame_width, frame_height, num_rows, num_cols, frame_rate):

        # Load sprite sheet
        self.__sheet = pygame.image.load(filename)

        # Dimensions of each frame in the sprite sheet
        self.__frame_width = frame_width
        self.__frame_height = frame_height

        # Number of rows and columns in the sprite sheet
        self.__num_rows = num_rows
        self.__num_cols = num_cols

        # Calculate total number of frames in the sprite sheet
        self.__num_frames = num_rows * num_cols

        # Create list to store each frame as a surface
        self.__frames = []
        self.__frame_rate = frame_rate
        self.__current_frame_index = 0
        self.__start = True

    '''gets anchor point for rotation, for now fits only for the flame thrower. might change in the future.'''

    def get_pivot(self):
        return self.__frame_width // 2, self.__frame_height

    '''this method should be run from the outside - it fills the frame list from sprite
        and returns the first frame from the recent made list - ready to be displayed
        from the calling class - assign self.image for this method output'''

    def fill_frames_and_get_first_frame(self):
        for row in range(self.__num_rows):
            for col in range(self.__num_cols):
                x = col * self.__frame_width
                y = row * self.__frame_height
                frame = pygame.Surface((self.__frame_width, self.__frame_height), pygame.SRCALPHA)
                frame.blit(self.__sheet, (0, 0), (x, y, self.__frame_width, self.__frame_height))
                self.__frames.append(frame)
        return self.__get_current_frame()

    '''this method is for testing only, it runs the animation from inside the class.
    the coordinates input is tuple of (x,y) and determine where the flame will be displayed on screen'''

    def __run(self, coordinates):
        pygame.init()
        win = pygame.display.set_mode((640, 480))
        self.fill_frames_and_get_first_frame()

        # Set up animation parameters
        current_time = pygame.time.get_ticks()

        # Main game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            current_frame, current_time = self.update_animation_frame(current_time)

            # Display current frame
            self.__draw(current_frame, coordinates, win)
            pygame.display.flip()

        pygame.quit()

    '''aid function to make sure the flame frames transition at the determined frame rate'''

    def __check_time_for_next_frame(self, time_since_last_frame):
        if time_since_last_frame > 1000 / self.__frame_rate:
            return True
        return False

    '''this function is responsible for the transition from the current frame to the next one, needs to be public
    it returns the desired frame, and the time of transition for further checkups'''

    def update_animation_frame(self, initial_time):
        current_time = pygame.time.get_ticks()
        time_since_last_frame = current_time - initial_time
        current_frame = self.__get_current_frame()
        if self.__check_time_for_next_frame(time_since_last_frame):
            current_frame = self.__get_next_frame()
            initial_time = current_time

        return current_frame, initial_time

    '''this method returns current frame'''

    def __get_current_frame(self):
        return self.__frames[self.__current_frame_index]

    '''this method returns the next frame, and resets the frame index is necessary for looping'''

    def __get_next_frame(self):
        self.__current_frame_index += 1
        self.__current_frame_index %= len(self.__frames)
        '''the commended code is in case i would like to make the sprite appearance gradual, currently not in use'''
        # if self.__current_frame_index == 0 and self.__start:
        #     self.__frames = self.__frames[10:]
        #     self.__start = False
        return self.__frames[self.__current_frame_index]

    '''drawing method - is used internally for testing (called by run)'''

    def __draw(self, current_frame, coordinates, win):
        win.fill((0, 0, 0))
        win.blit(current_frame, coordinates)


'''internal activation examples'''
# x = Sprite("flame001.png", 93, 216, 15, 5, 25)
# x.run((100,100))

# x2 = Sprite("flame002.png", 181, 404, 10, 5, 40)
# x2.run((120, 40))