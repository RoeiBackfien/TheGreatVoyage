import pygame as py


class Character:
    def __init__(self, img, x, y):
        self.name = img.split('\\')[8]
        self.img = py.image.load(img).convert()
        self.rect = self.img.get_rect()
        self.x = x
        self.y = y

    def draw(self, screen):
        self.img.set_colorkey((255, 255, 255))
        screen.blit(self.img, (self.x, self.y))

    def __str__(self):
        return self.name
