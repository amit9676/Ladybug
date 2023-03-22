WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

def keep_inside_boundries(left,right,top,buttom):
    if left < 0:
        self.rect.left = 0
    if self.rect.right > WINDOW_WIDTH:
        self.rect.right = WINDOW_WIDTH
    if self.rect.top < 0:
        self.rect.top = 0
    if self.rect.bottom > WINDOW_HEIGHT:
        self.rect.bottom = WINDOW_HEIGHT