import math
import pygame
from spriteTest import Sprite

def blitRotate(surf, image, pos, originPos, angle):
    image_rect = image.get_rect(topleft = (pos[0] - originPos[0], pos[1]-originPos[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    rotated_image = pygame.transform.rotate(image, angle)

    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    surf.blit(rotated_image, rotated_image_rect)

pygame.init()
size = (800,800)
middle = (size[0] // 2, size[1] // 2)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

#image = pygame.image.load("flame001.gif")
spr = Sprite("flame002.png", 181, 404, 10, 5, 40)
image = spr.fill_frames_and_get_first_frame()
pivot = spr.get_pivot()
print(pivot)

angle = 90
pos = [middle[0] + math.cos(math.radians(angle))*50, middle[1] - math.sin(math.radians(angle))*50]
rotate_speed = 3
done = False
right_pressed = False
left_pressed = False
current_time = pygame.time.get_ticks()
while not done:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                right_pressed = True
            elif event.key == pygame.K_LEFT:
                left_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                right_pressed = False
            elif event.key == pygame.K_LEFT:
                left_pressed = False

    screen.fill(0)

    if right_pressed:
        angle -= rotate_speed
        angle %= 360
        pos[0] = middle[0] + math.cos(math.radians(angle))*50 #x value
        pos[1] = middle[1] - math.sin(math.radians(angle))*50  # y value, crosshair moves right when rotating right
    if left_pressed:
        angle += rotate_speed
        angle %= 360
        pos[0] = middle[0] + math.cos(math.radians(angle))*50
        pos[1] = middle[1] - math.sin(math.radians(angle))*50  # crosshair moves left when rotating left

    print(f"{angle}, {math.radians(angle)}")
    blitRotate(screen, image, pos, pivot, angle-90)

    #image = spr.get_next_frame()
    #current_time = pygame.time.get_ticks()
    #time = current_time - original_time
    image, current_time = spr.update_animation_frame(current_time)

    pygame.draw.line(screen, (0, 255, 0), (pos[0]-20, pos[1]), (pos[0]+20, pos[1]), 3)
    pygame.draw.line(screen, (0, 255, 0), (pos[0], pos[1]-20), (pos[0], pos[1]+20), 3)
    pygame.draw.circle(screen, (0, 255, 0), pos, 7, 0)
    pygame.draw.circle(screen, (0, 255, 0), (middle[0], middle[1]), 50, 1)
    pygame.draw.circle(screen, (220, 255, 0), (middle[0], middle[1]), 7, 0)

    pygame.display.flip()

pygame.quit()
exit()
