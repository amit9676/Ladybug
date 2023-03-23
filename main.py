import math
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


def trigo(direction, speed, current_x, current_y):
    dx = math.sin(math.radians(direction)) * speed
    dy = math.cos(math.radians(direction)) * speed



    # Update the ladybug's position
    return current_x + dx, current_y - dy, round(current_x + dx), round(current_y - dy)

    # self.current_x += dx
    # self.current_y -= dy
    #
    # self.rect.x = round(self.current_x)
    # self.rect.y = round(self.current_y)

