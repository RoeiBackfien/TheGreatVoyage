import pygame as py


class Character:
    def __init__(self, img, x, y, name):
        self.name = name
        self.img = img
        self.x = x
        self.y = y

    def __str__(self):
        return self.name
