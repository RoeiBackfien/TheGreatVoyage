import pygame
from abc import *


class Tile(ABC):

    def __init__(self, x, y):
        self.radius = 30
        self.x = x
        self.y = y
        self.color = None

    @abstractmethod
    def draw(self, screen):
        pass


class GoldTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 250, 100)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)


class FightTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 250, 100)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)


class MedalTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 250, 100)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)


class FateMaskTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 250, 100)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)


class StoryTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 250, 100)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)


class LoseGoldTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 250, 100)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)


class AnotherTurnTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 250, 100)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)


class FreezeTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 250, 100)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)


class ReverseTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 250, 100)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)
