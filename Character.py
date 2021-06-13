import pygame as py


class Character:
    def __init__(self, x, y, name, color):
        self.name = name
        self.x = x
        self.y = y
        self.width = 20
        self.height = 30
        self.color = color

    def __str__(self):
        return self.name
