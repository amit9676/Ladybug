import pygame


class Sprite:
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

    def get_pivot(self):
        return self.__frame_width // 2, self.__frame_height

    def fill_frames_and_get_first_frame(self):
        for row in range(self.__num_rows):
            for col in range(self.__num_cols):
                x = col * self.__frame_width
                y = row * self.__frame_height
                frame = pygame.Surface((self.__frame_width, self.__frame_height), pygame.SRCALPHA)
                frame.blit(self.__sheet, (0, 0), (x, y, self.__frame_width, self.__frame_height))
                self.__frames.append(frame)
        return self.get_current_frame()

    def __run(self,coordinates): #this method is for testing only, it runs the animation from inside the class
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
            self.draw(current_frame, coordinates, win)
            pygame.display.flip()

        pygame.quit()

    def __check_time_for_next_frame(self, time_since_last_frame):
        if time_since_last_frame > 1000 / self.__frame_rate:
            return True
        return False

    def update_animation_frame(self,initial_time):
        current_time = pygame.time.get_ticks()
        time_since_last_frame = current_time - initial_time
        current_frame = self.get_current_frame()
        if self.__check_time_for_next_frame(time_since_last_frame):
            current_frame = self.get_next_frame()
            initial_time = current_time

        return current_frame, initial_time

    def get_current_frame(self):
        return self.__frames[self.__current_frame_index]

    def get_next_frame(self):
        #self.current_frame_index = (self.current_frame_index + 1) % len(self.frames)
        self.__current_frame_index += 1
        self.__current_frame_index %= len(self.__frames)
        return self.__frames[self.__current_frame_index]

    def draw(self, current_frame, coordinates, win):
        win.fill((0, 0, 0))
        win.blit(current_frame, coordinates)



#x = Sprite("flame001.png", 93, 216, 15, 5, 25)
#x.run((100,100))

#x2 = Sprite("flame002.png", 181, 404, 10, 5, 40)
#x2.run((120, 40))
