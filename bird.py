import random
from parameters import *
from images import *


class Bird:
    def __init__(self, away_y):
        self.x = random.randrange(550, 730)
        self.y = away_y
        self.width = 55
        self.height = 105
        self.ay = away_y
        self.speed = 3
        self.dest_y = self.speed * random.randrange(20, 70)
        self.img_cnt = 0
        self.cd_hide = 0
        self.come = True
        self.go_away = False

    def draw(self):
        if self.img_cnt == 30:
            self.img_cnt = 0

        display.blit(bird_img[self.img_cnt // 6], (self.x, self.y))
        self.img_cnt += 1

        if self.come and self.cd_hide == 0:
            return 1
        elif self.go_away:
            return 2
        elif self.cd_hide > 0:
            self.cd_hide -= 1

        return 0

    def show(self):
        if self.y < self.dest_y:
            self.y += self.speed
        else:
            self.come = False
            # self.go_away = True
            self.dest_y = self.ay

    def hide(self):
        if self.y > self.dest_y:
            self.y -= self.speed
        else:
            self.come = True
            self.go_away = False
            self.x = random.randrange(550, 730)
            self.dest_y = self.speed * random.randrange(20, 70)

    def check_dmg(self, bullet):
        if self.x <= bullet.x <= self.x + self.width:
            if self.y <= bullet.y <= bullet.y + self.height:
                self.go_away = True