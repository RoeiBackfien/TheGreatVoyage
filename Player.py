from Tile import *
import random
from enum import Enum


class Direction(Enum):
    FORWARD = 0
    BACKWARD = 1
    NONE = 2


class Player:
    def __init__(self, character):
        self.character = character
        self.gold = 0
        self.battles_won = 0
        self.fate_masks = 0
        self.medals = 0
        self.currentTile = None
        self.direction = Direction.NONE

    def __init__(self):
        self.character = None
        self.gold = 0
        self.battles_won = 0
        self.fate_masks = 0
        self.medals = 0
        self.currentTile = None
        self.direction = Direction.NONE

    def update(self, tile):
        if type(tile) == GoldTile:
            self.gold += 10
        elif type(tile) == FateMaskTile:
            num = random.randint(1, 7)
            if num < 3:
                pass
            elif num == 3:
                pass
            else:
                self.fate_masks += 1
            pass
        elif type(tile) == FightTile:
            pass
        elif type(tile) == LoseGoldTile:
            self.gold -= 10
        elif type(tile) == StoryTile:
            num = random.randint(1, 7)
        elif type(tile) == FreezeTile:
            self.direction = Direction.NONE
        elif type(tile) == AnotherTurnTile:
            self.direction = Direction.FORWARD
        elif type(tile) == ReverseTile:
            self.direction = Direction.BACKWARD

    def move(self, times, tiles):
        for i in range(times):
            self.currentTile = tiles[self.currentTile + 1]
