import pygame
from abc import *


class Tile(ABC):

    def __init__(self, x, y):
        self.radius = 27
        self.x = x
        self.y = y
        self.color = (0, 0, 0)

    @abstractmethod
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)


class GoldTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 255, 0)

    def draw(self, screen):
        super(GoldTile, self).draw(screen)


class FightTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 250, 100)

    def draw(self, screen):
        super(FightTile, self).draw(screen)


class MedalTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 250, 100)

    def draw(self, screen):
        super(MedalTile, self).draw(screen)


class FateMaskTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (0, 0, 0)

    def draw(self, screen):
        super(FateMaskTile, self).draw(screen)


class StoryTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (51, 255, 51)

    def draw(self, screen):
        super(StoryTile, self).draw(screen)


class LoseGoldTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (204, 0, 0)

    def draw(self, screen):
        super(LoseGoldTile, self).draw(screen)


class AnotherTurnTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (51, 255, 51)

    def draw(self, screen):
        super(AnotherTurnTile, self).draw(screen)


class FreezeTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (0, 255, 255)

    def draw(self, screen):
        super(FreezeTile, self).draw(screen)


class ReverseTile(Tile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (51, 255, 51)

    def draw(self, screen):
        super(ReverseTile, self).draw(screen)
