import pygame


class Sprite:
    def __init__(self, filename, frame_width, frame_height, num_rows, num_cols, frame_rate):
        pygame.init()
        self.win = pygame.display.set_mode((640, 480))

        # Load sprite sheet
        self.sheet = pygame.image.load("flame001.png")

        # Dimensions of each frame in the sprite sheet
        self.frame_width = frame_width
        self.frame_height = frame_height

        # Number of rows and columns in the sprite sheet
        self.num_rows = num_rows
        self.num_cols = num_cols

        # Calculate total number of frames in the sprite sheet
        self.num_frames = num_rows * num_cols

        # Create list to store each frame as a surface
        self.frames = []
        self.frame_rate = frame_rate

    def run(self):
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                x = col * self.frame_width
                y = row * self.frame_height
                frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
                frame.blit(self.sheet, (0, 0), (x, y, self.frame_width, self.frame_height))
                self.frames.append(frame)

        # Set up animation parameters
        frame_index = 0
        last_frame_time = pygame.time.get_ticks()

        # Main game loop
        running = True
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update animation frame
            current_time = pygame.time.get_ticks()
            time_since_last_frame = current_time - last_frame_time
            if time_since_last_frame > 1000 / self.frame_rate:
                frame_index = (frame_index + 1) % self.num_frames
                last_frame_time = current_time

            # Display current frame
            current_frame = self.frames[frame_index]
            self.win.fill((0, 0, 0))
            self.win.blit(current_frame, (100, 100))
            pygame.draw.circle(self.win, (220, 255, 0), (200, 200), 7, 0)
            pygame.display.flip()

        pygame.quit()


x = Sprite("flame001.png", 93, 216, 15, 5, 20)
x.run()
