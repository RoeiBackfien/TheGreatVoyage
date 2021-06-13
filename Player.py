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
        self.num = -1
        self.path = None

    def update(self):
        if type(self.currentTile) == GoldTile:
            self.gold += 10
        elif type(self.currentTile) == LoseGoldTile:
            if self.gold != 0:
                self.gold -= 10
        elif type(self.currentTile) == FreezeTile:
            self.direction = Direction.NONE
        elif type(self.currentTile) == MedalTile:
            self.medals += 1
        elif type(self.currentTile) == AnotherTurnTile:
            self.direction = Direction.FORWARD
        elif type(self.currentTile) == ReverseTile:
            self.direction = Direction.BACKWARD
        elif type(self.currentTile) == EndTile:
            self.medals += 1

    def play(self, game, p2, num):
        done = False
        broke = False
        try:
            index = 0
            for i in range(len(self.path)):
                if self.path[i] == self.currentTile:
                    index = i
                    break
            for j in range(num):
                if self.direction == Direction.FORWARD:
                    if index != len(self.path) - 1:
                        self.currentTile = self.path[index + 1]
                    else:
                        done = True
                        print('done')
                        break
                    index += 1
                    game.move_character(self.character, self.currentTile.x, self.currentTile.y, p2.character)
                elif self.direction == Direction.BACKWARD:
                    if index != 0:
                        self.currentTile = self.path[index - 1]
                        index -= 1
                        game.move_character(self.character, self.currentTile.x, self.currentTile.y, p2.character)
                    else:
                        broke = True
                        break
                elif self.direction == Direction.NONE:
                    broke = True
                    break
            self.direction = Direction.FORWARD
            if not broke:
                self.update()
            if done:
                return True
        except Exception as e:
            print(e)
            pass
