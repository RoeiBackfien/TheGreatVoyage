from Tile import *
import random
from enum import Enum


class Direction(Enum):
    FORWARD = 0
    BACKWARD = 1
    NONE = 2


class Player:
    def __init__(self):
        self.character = None
        self.play = False
        self.gold = 0
        self.battles_won = 0
        self.fate_masks = 0
        self.medals = 0
        self.currentTile = None
        self.direction = Direction.NONE

    def update(self):
        if type(self.currentTile) == GoldTile:
            self.gold += 10
        elif type(self.currentTile) == FateMaskTile:
            num = random.randint(1, 7)
            if num < 3:
                pass
            elif num == 3:
                pass
            else:
                self.fate_masks += 1
            pass
        elif type(self.currentTile) == FightTile:
            pass
        elif type(self.currentTile) == LoseGoldTile:
            self.gold -= 10
        elif type(self.currentTile) == StoryTile:
            num = random.randint(1, 7)
        elif type(self.currentTile) == FreezeTile:
            self.direction = Direction.NONE
        elif type(self.currentTile) == AnotherTurnTile:
            self.direction = Direction.FORWARD
        elif type(self.currentTile) == ReverseTile:
            self.direction = Direction.BACKWARD

    def play(self, tiles):
        num = random.randint(1, 7)
        for i in range(num):
            self.currentTile = tiles[self.currentTile + 1]
        self.update()
