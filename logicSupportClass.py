import math
import pygame
import random

'''logic operations class - this class contains method which are used by multiple classes.
it is a support class containing logic operations used by various units, projectile and objects in general in the game.'''


class LogicSupportClass:
    def __init__(self):
        self.__WINDOW_WIDTH = 1000
        self.__WINDOW_HEIGHT = 750
        self.winMode = True

    def get_window(self):
        return self.__WINDOW_WIDTH, self.__WINDOW_HEIGHT

    def get_flamethrower_range(self):
        return 216

    def advance(self, direction: int, speed: float, current_x: float, current_y: float) -> (float, float, int, int):
        dx = math.sin(math.radians(direction)) * speed
        dy = math.cos(math.radians(direction)) * speed
        # Update the  position
        return current_x + dx, current_y - dy, round(current_x + dx), round(current_y - dy)

    def initilize_currents(self, x, y) -> (float, float):
        return float(x), float(y)

    def draw(self, surface: pygame.surface, image: pygame.surface, rect: pygame.rect):
        # Draw the image on the surface
        surface.blit(image, rect)

    '''this method is responsible for rotating an image as we will.
    image argument its the the image we would like to rotate.
    pos is (x,y) tuple of to where place the pivot of the image on the screen.
    pivot is (x,y) tuple - the point on image that would be used as rotation anchor-the image will be rotated around it.
    angle is the rotation angle, based on mathematical axis graph.
    the output is the rotation image, and the rectangle of it.
    it was made with the help of
    https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame'''

    def blitRotate(self, image, pos: (int, int), pivot: (int,int), angle: int) -> (pygame.surface, pygame.rect):
        angle -= 90
        image_rect = image.get_rect(topleft=(pos[0] - pivot[0], pos[1] - pivot[1]))
        offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
        rotated_offset = offset_center_to_pivot.rotate(-angle)
        rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
        rotated_image = pygame.transform.rotate(image, angle)

        rotated_image_rect = rotated_image.get_rect(center=rotated_image_center)
        return rotated_image, rotated_image_rect

    '''this method is required to convert the game directions (which 0 degrees is up arrow) - to mathematical
    angles which are needed for the rotation calculations, which are based on radians, circles and trigonometry.'''

    def game_to_graph_axis_degrees(self, direction: int) -> int:
        return (90 - direction) % 360

    '''check if game instance crossed the boundries'''
    def check_for_boundary_crossing(self, rect: pygame.rect, window: (int,int)) -> bool:
        if rect.right < 0 or rect.left > window[0] or rect.bottom < 0 \
                or rect.top > window[1]:
            return True
        return False

    '''based on unit speed and direction - calculate the velocity of which for each direction - meaning how fast
    it moves on the X axis, and how fast it moves on the white axis.
    note: function does NOT considers any boundaries - that must be handles and adjusted in the  specific unit class.
    
    note 2: the direction input is mathematical graph degrees, not pygame degrees. '''
    def calculate_velocity(self, speed: float, direction: int) -> (float, float):
        # Convert direction from degrees to radians
        radians = math.radians(direction)

        # Calculate the velocity components
        velocityX = speed * math.cos(radians)
        velocityY = speed * math.sin(radians)

        return velocityX, velocityY * -1

    '''given position, direction and radius - return position that is at distance of radius at the
    given direction'''
    def circular_emergernce_position(self, position: (int, int), direction: int, radius: int) -> (int,int):
        return [position[0] + math.cos(math.radians(direction)) * radius,
                position[1] - math.sin(math.radians(direction)) * radius]


    '''methods required for check collision between 2 objects - it has 2 methods: impact identifier
    and __check_collision.
    impact_identifier - get called by the caller - an object does checks for collision
    the caller can be a projectile (missile, flamethrower, sniper or fireball) or warwagon.
    the caller constantly checks if there is a colision between the caller and the instances - if it does,
     for a projectile it means it hit its target.
     and for the warwagon it means it runs the target over.     
     the function might have some variants in the future - fireball and sniper can hit only one enemy.
     sniper can hit only units from the other team (no friendly fire)
     currently the function returns a list of objects in which there was an impact on them
     
     __check_collision - a private method called  by the impact_identifier - it is the function that makes the actual
     checking for collision - it takes the 2 objects it wants to check - first it checks rectangle collision by
     calling every instance 'get_rect() method. if that checks out - it means that the rectangles overlap, however
     that by itself does not means there is indeed an impact, so there is a verification check - in which the function
     calls the objects 'get_mask() for check if they overlap - if they does - it means the object's images overlap -
     meaning impact!'''
    def __check_collision(self, obj1, obj2):
        """
        Checks for collision between two objects using masks.
        """
        # Check for rect collision first
        if obj1.get_rect().colliderect(obj2.get_rect()):
            # If rect collision occurs, check for mask collision
            offset = (obj2.get_rect().left - obj1.get_rect().left, obj2.get_rect().top - obj1.get_rect().top)
            if obj1.get_mask().overlap(obj2.get_mask(), offset):
                return True
        return False

    '''projectile - the object that is used as projectile (or war wagon) - meaning the object that does the hitting
        it is the equivalent of bullet.
        
        caller - the object that sent the projectile - equivalent of gun, in case of war wagon - it will be itself
        
        game - the game object, with the data on current instances on screen'''
    def impact_identifier(self,projectile, caller, instances):
        impacted = []
        # instances = []
        # instances += game.get_inctances()
        # instances += game.get_wagons()
        for ins in instances:
            if ins == caller:
                continue
            res = self.__check_collision(projectile, ins)
            if res:
                impacted.append(ins)
        return impacted

    '''currently un-used, might change in the future'''
    def get_random_int(self, low: int, high: int) -> int:
        return random.randint(low, high)

    def generate_random_location(self,window) -> (int,int):
        width = self.get_random_int(0,window[0])
        height = self.get_random_int(1,window[1])
        return width, height
