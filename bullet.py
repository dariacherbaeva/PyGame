from parameters import *
from images import *

pygame.init()


class Bullet:
    def __init__(self, x, y):
        self.speed = None
        self.x = x
        self.y = y
        self.speed_x = 8
        self.speed_y = 0
        self.dest_x = 0
        self.dest_y = 0

    def move(self):
        self.x += self.speed
        if self.x <= display_width:
            display.blit(bullet_img, (self.x, self.y))
            return True
        else:
            return False

    def find_path(self, dest_x, dest_y):
        self.dest_x = dest_x
        self.dest_y = dest_y

        delta_x = dest_x - self.x
        count_up = delta_x // self.speed_x
        if self.y >= dest_y:
            delta_y = self.y - dest_y
            self.speed_y = delta_y / count_up
        else:
            delta_y = dest_y - self.y
            self.speed_y = -(delta_y / count_up)

    def move_to(self):
        self.x += self.speed_x
        self.y -= self.speed_y
        if self.x <= display_width and self.y >= 0:
            display.blit(bullet_img, (self.x, self.y))
            return True
        else:
            return False