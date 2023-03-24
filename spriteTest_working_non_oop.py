import pygame

pygame.init()
win = pygame.display.set_mode((640, 480))

# Load sprite sheet
sheet = pygame.image.load("flame001.png")

# Dimensions of each frame in the sprite sheet
frame_width = 93
frame_height = 216

# Number of rows and columns in the sprite sheet
num_rows = 15
num_cols = 5

# Calculate total number of frames in the sprite sheet
num_frames = num_rows * num_cols

# Create list to store each frame as a surface
frames = []
for row in range(num_rows):
    for col in range(num_cols):
        x = col * frame_width
        y = row * frame_height
        frame = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
        frame.blit(sheet, (0, 0), (x, y, frame_width, frame_height))
        frames.append(frame)

# Set up animation parameters
frame_index = 0
frame_rate = 20 # frames per second
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
    if time_since_last_frame > 1000 / frame_rate:
        frame_index = (frame_index + 1) % num_frames
        last_frame_time = current_time

    # Display current frame
    current_frame = frames[frame_index]
    win.fill((0, 0, 0))
    win.blit(current_frame, (0, 0))
    pygame.display.flip()

pygame.quit()
