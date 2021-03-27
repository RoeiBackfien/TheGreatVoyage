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
        self.gold = 0
        self.battles_won = 0
        self.fate_masks = 0
        self.medals = 0
        self.currentTile = None
        self.direction = Direction.NONE
        self.connected = False
        self.turn = False

    def update(self):
        if type(self.currentTile) == GoldTile:
            self.gold += 10
        elif type(self.currentTile) == FateMaskTile:
            num = random.randint(1, 6)
            # num = cube.temp(screen)
            if num < 3:
                pass
            elif num == 3:
                pass
            else:
                self.fate_masks += 1
        elif type(self.currentTile) == FightTile:
            pass
        elif type(self.currentTile) == LoseGoldTile:
            self.gold -= 10
        elif type(self.currentTile) == StoryTile:
            # num = random.randint(1, 6)
            pass
        elif type(self.currentTile) == FreezeTile:
            self.direction = Direction.NONE
        elif type(self.currentTile) == AnotherTurnTile:
            self.direction = Direction.FORWARD
        elif type(self.currentTile) == ReverseTile:
            self.direction = Direction.BACKWARD

    def play(self, tiles, num):
        if self.turn:
            try:
                index = 0
                for i in range(len(tiles)):
                    if tiles[i] == self.currentTile:
                        index = i
                for j in range(num):
                    self.currentTile = tiles[index + 1]
                self.update()
                return self.currentTile.x, self.currentTile.y
            except Exception as e:
                print(e)
