from Tile import *
from enum import Enum


class Direction(Enum):
    FORWARD = 0
    BACKWARD = 1
    NONE = 2


class Player:
    def __init__(self):
        self.character = None
        self.gold = 0
        self.medals = 0
        self.currentTile = None
        self.direction = Direction.FORWARD
        self.connected = False
        self.turn = False
        self.num = -1

    def update(self):
        if type(self.currentTile) == GoldTile:
            self.gold += 10
        elif type(self.currentTile) == LoseGoldTile:
            self.gold -= 10
        elif type(self.currentTile) == FreezeTile:
            self.direction = Direction.NONE
        elif type(self.currentTile) == MedalTile:
            self.medals += 1
        elif type(self.currentTile) == AnotherTurnTile:
            self.direction = Direction.FORWARD
        elif type(self.currentTile) == ReverseTile:
            self.direction = Direction.BACKWARD

    def play(self, tiles):
        try:
            index = 0
            for i in range(len(tiles)):
                if tiles[i] == self.currentTile:
                    index = i
            if self.direction == Direction.FORWARD:
                self.currentTile = tiles[index + 1]
            elif self.direction == Direction.BACKWARD:
                self.currentTile = tiles[index - 1]
                self.direction = Direction.FORWARD
            return self.currentTile.x, self.currentTile.y
        except:
            pass
