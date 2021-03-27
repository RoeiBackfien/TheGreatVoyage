import random
import pygame as py
import time


def rotate(img, angle):
    rotated_surface = py.transform.rotozoom(img, angle, 1)
    rotated_rect = rotated_surface.get_rect(center=(300, 300))
    return rotated_surface, rotated_rect


def clicked(event):
    return event.type == py.MOUSEBUTTONDOWN and event.button == 1


class Cube:
    root = 'D:\School\\2020-21\Cyber\Ofir\Work\TheGreatVoyage\\Pictures\\'
    cube1 = root + 'cube1.png'
    cube2 = root + 'cube2.png'
    cube3 = root + 'cube3.png'
    cube4 = root + 'cube4.png'
    cube5 = root + 'cube5.png'
    cube6 = root + 'cube6.png'

    def __init__(self):
        self.positions = [self.cube1, self.cube1, self.cube1, self.cube1, self.cube1, self.cube1]
        self.transform = {1: self.cube1, 2: self.cube1, 3: self.cube1, 4: self.cube1, 5: self.cube1, 6: self.cube1}
        self.should_keep_rolling = True
        self.angle = 0

    def start(self):
        self.screen = py.display.set_mode((600, 600))
        py.display.set_caption("Game")

    # def roll_periodic(self):
    #    for pos in self.positions:
    #        self.screen.fill((100, 100, 100))
    #        img = py.image.load(pos)
    #        img_rotated, rotated_rect = rotate(img, self.angle)
    #        img_rotated.set_colorkey((255, 255, 255))
    #        self.screen.blit(img_rotated, rotated_rect)
    #        py.display.flip()
    #        self.clock.tick(60)
    #        self.angle += 7
    def draw(self, screen):
        img = py.image.load(self.positions[0])
        img.set_colorkey((255, 255, 255))
        screen.blit(img, (20, 50))
        py.display.flip()

    def roll_on_click(self):
        num = 1  # random.randint(1, 6)
        print(num)
        desired_angle = 370
        i = 1
        while self.angle != desired_angle:  # does a full spin and gets to the pos
            if i == 7:
                i = 1
            self.screen.fill((100, 100, 100))
            img = py.image.load(self.transform[i])
            img_rotated, rotated_rect = rotate(img, self.angle)
            img_rotated.set_colorkey((255, 255, 255))
            self.screen.blit(img_rotated, rotated_rect)
            py.display.flip()
            self.angle += 10
            i += 1
        for j in range(1, num + 1):
            self.screen.fill((100, 100, 100))
            img = py.image.load(self.transform[j])
            img_rotated, rotated_rect = rotate(img, self.angle)
            img_rotated.set_colorkey((255, 255, 255))
            self.screen.blit(img_rotated, rotated_rect)
            py.display.flip()
            self.angle += 10 + (360 / num)

    def temp(self, screen):
        py.draw.rect(screen, (0, 100, 255), (20, 20, 80, 60))
        num = random.randint(1, 6)
        font = py.font.SysFont("comicsans", 60)
        text = font.render(str(num), True, (0, 255, 255))
        screen.blit(text, (50, 30))
        return num

# py.init()
# c = Cube()
# c.start()
# c.roll_on_click()
# while True:
#    pass
