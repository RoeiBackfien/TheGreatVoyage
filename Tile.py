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

    @abstractmethod
    def __str__(self):
        return 'Tile'


class StartTile(Tile):
    def __str__(self):
        return 'StartTile'

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (0, 102, 102)

    def draw(self, screen):
        super(StartTile, self).draw(screen)


class GoldTile(Tile):
    def __str__(self):
        return 'GoldTile'

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 255, 0)

    def draw(self, screen):
        super(GoldTile, self).draw(screen)


class MedalTile(Tile):
    def __str__(self):
        return 'MedalTile'

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 250, 100)

    def draw(self, screen):
        super(MedalTile, self).draw(screen)


class LoseGoldTile(Tile):
    def __str__(self):
        return 'LoseGoldTile'

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (204, 0, 0)

    def draw(self, screen):
        super(LoseGoldTile, self).draw(screen)


class AnotherTurnTile(Tile):
    def __str__(self):
        return 'AnotherTurnTile'

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (51, 255, 51)

    def draw(self, screen):
        super(AnotherTurnTile, self).draw(screen)


class FreezeTile(Tile):
    def __str__(self):
        return 'FreezeTile'

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (0, 255, 255)

    def draw(self, screen):
        super(FreezeTile, self).draw(screen)


class ReverseTile(Tile):
    def __str__(self):
        return 'ReverseTile'

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (51, 255, 51)

    def draw(self, screen):
        super(ReverseTile, self).draw(screen)


class EndTile(Tile):
    def __str__(self):
        return 'EndTile'

    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 255, 255)

    def draw(self, screen):
        super(EndTile, self).draw(screen)
