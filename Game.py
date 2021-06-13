import pygame as py
from Character import Character
from Tile import *
from Button import Button
from Player import Player
from Cube import Cube
import time
import os

root = os.getcwd() + '\\Pictures\\'
end = '.png'
start_img = root + 'start' + end
map_img = root + 'map' + end
gold_img = root + 'gold' + end
medal_img = root + 'medal' + end


def clicked(event):
    return event.type == py.MOUSEBUTTONDOWN and event.button == 1


class Game:

    def __init__(self, id):
        self.id = id
        self.width = 1700
        self.height = 900
        self.size = (self.width, self.height)

        self.screen = None
        self.font = None
        self.ready = False

        self.characters_buttons = [Button(100, 700, 300, 100, (200, 150, 150), 'Choose'),
                                   Button(600, 700, 300, 100, (200, 150, 150), 'Choose'),
                                   Button(1150, 700, 300, 100, (200, 150, 150), 'Choose')]

        self.start_button = Button(600, 700, 300, 100, (200, 150, 150), 'Start')
        self.instructions_button = Button(600, 700, 300, 100, (200, 150, 150), 'Instructions')

        self.start_tiles = [StartTile(50, 210), GoldTile(150, 210)]

        self.first_split_1 = [FreezeTile(150, 320), ReverseTile(150, 420), GoldTile(150, 520), LoseGoldTile(250, 522),
                              ReverseTile(360, 522), LoseGoldTile(470, 522)]

        self.first_split_2 = [GoldTile(250, 210), FreezeTile(330, 270), AnotherTurnTile(420, 335),
                              LoseGoldTile(510, 410)]

        self.mid_tiles = [GoldTile(570, 522), FreezeTile(680, 522), MedalTile(780, 522)]

        self.second_split_1 = [GoldTile(720, 610), LoseGoldTile(640, 650), FreezeTile(550, 660), LoseGoldTile(450, 660),
                               GoldTile(350, 660), LoseGoldTile(250, 660), ReverseTile(160, 700), GoldTile(170, 790),
                               FreezeTile(270, 810), LoseGoldTile(370, 815), GoldTile(470, 815), ReverseTile(600, 815),
                               GoldTile(700, 815), GoldTile(800, 815), FreezeTile(900, 815), GoldTile(1000, 815),
                               GoldTile(1100, 815), GoldTile(1200, 815), GoldTile(1300, 815), LoseGoldTile(1380, 740),
                               LoseGoldTile(1380, 640), LoseGoldTile(1380, 540), LoseGoldTile(1380, 440)]

        self.second_split_2 = [GoldTile(880, 522), LoseGoldTile(850, 440), FreezeTile(795, 370), GoldTile(750, 290),
                               LoseGoldTile(710, 200), GoldTile(810, 180), FreezeTile(910, 180), ReverseTile(1100, 180),
                               GoldTile(1200, 180), FreezeTile(1300, 180), ReverseTile(1380, 180), GoldTile(1380, 260)]

        self.end_tiles = [FreezeTile(1380, 340), GoldTile(1480, 340), EndTile(1580, 340)]

        # Paths
        self.first_first = self.start_tiles + self.first_split_1 \
                           + self.mid_tiles + self.second_split_1 + self.end_tiles

        self.first_second = self.start_tiles + self.first_split_1 \
                            + self.mid_tiles + self.second_split_2 + self.end_tiles

        self.second_first = self.start_tiles + self.first_split_2 \
                            + self.mid_tiles + self.second_split_1 + self.end_tiles

        self.second_second = self.start_tiles + self.first_split_2 \
                             + self.mid_tiles + self.second_split_2 + self.end_tiles

        self.paths = [self.first_first, self.first_second, self.second_first, self.second_second]

        self.cube = Cube(0, 0, (255, 50, 0))
        self.current_player_num = -1
        self.players = [Player(), Player()]
        self.characters = [Character(220, 400, 'red', (255, 0, 0), 30), Character(765, 400, 'green', (0, 255, 0), 40),
                           Character(1300, 400, 'blue', (0, 0, 255), 50)]

    def initialize(self):
        py.init()
        py.font.init()
        self.font = pygame.font.SysFont("comicsans", 60)
        self.screen = py.display.set_mode(self.size)
        py.display.set_caption("Game")

    def choose_character(self, event):
        characters = {self.characters_buttons[0].x: self.characters[0],
                      self.characters_buttons[1].x: self.characters[1],
                      self.characters_buttons[2].x: self.characters[2]}
        for btn in self.characters_buttons:
            if btn.clicked_on(event):
                return True, characters[btn.x]

    def move_character(self, character, des_x, des_y, other_character):
        x = character.x
        y = character.y
        y_diff = (des_y - y)
        x_diff = (des_x - x)

        if x_diff != 0 and y_diff != 0:
            while x != des_x and y != des_y:
                self.draw_field()
                x += x_diff
                y += y_diff
                character.x = x
                character.y = y
                self.draw_character(character)
                self.draw_character(other_character)
                time.sleep(0.6)
        elif x_diff == 0:
            while y != des_y:
                self.draw_field()
                y += y_diff
                character.y = y
                self.draw_character(character)
                self.draw_character(other_character)
                time.sleep(0.6)
        elif y_diff == 0:
            while x != des_x:
                self.draw_field()
                x += x_diff
                character.x = x
                self.draw_character(character)
                self.draw_character(other_character)
                time.sleep(0.6)

    def reset_screen(self):
        self.screen.fill((0, 0, 0))

    def is_players_connected(self):
        return self.players[0].connected and self.players[1].connected

    def players_ready(self):
        return self.players[0].character is not None and self.players[1].character is not None

    def start_characters(self):
        for player in self.players:
            player.character.x = 50
            player.character.y = 210
            self.draw_character(player.character)
            player.currentTile = player.path[0]

    def draw_character(self, character):
        rect = py.Surface((character.width, character.height))
        rect.fill(character.color)
        self.screen.blit(rect, (character.x, character.y))
        py.display.flip()

    def choose_menu(self):
        for character in self.characters:
            self.draw_character(character)

        for button in self.characters_buttons:
            button.draw(self.screen)

        text = self.font.render("Choose Your Champion", True, (0, 255, 255))
        self.screen.blit(text, (600, 100))
        py.display.flip()

    def get_character_by_name(self, name):
        for c in self.characters:
            if c.name == name:
                return c

    def disp_player(self, num):
        player = self.players[num]
        text = self.font.render(f" Player Number {player.num}", True, (0, 255, 255))
        self.screen.blit(text, (600, 20))

        img = py.image.load(gold_img).convert()
        img.set_colorkey((255, 255, 255))
        self.screen.blit(img, (200, 0))

        text = self.font.render(f" - {player.gold}", True, (0, 255, 255))
        self.screen.blit(text, (320, 20))

        img = py.image.load(medal_img).convert()
        img.set_colorkey((255, 255, 255))
        self.screen.blit(img, (400, 0))

        text = self.font.render(f" - {player.medals}", True, (0, 255, 255))
        self.screen.blit(text, (520, 20))
        py.display.flip()

    def draw_field(self):
        img = py.image.load(map_img).convert()
        img.set_colorkey((255, 255, 255))
        self.screen.blit(img, (0, 0))
        py.draw.rect(self.screen, (153, 76, 0), (0, 0, 1700, 120))

        for path in self.paths:
            for tile in path:
                tile.draw(self.screen)
        self.cube.draw(self.screen)
        py.display.flip()

    def main_menu(self):
        self.reset_screen()
        img = py.image.load(start_img)
        self.screen.blit(img, (0, 0))
        self.start_button.draw(self.screen)
        py.display.flip()

    def waiting_for_players_screen(self):
        self.reset_screen()
        text = self.font.render("Waiting For Players...", True, (0, 255, 255))
        self.screen.blit(text, (600, 100))
        py.display.flip()

    def checkWinningPlayer(self):
        self.reset_screen()
        gold_winner = self.players[0] if self.players[0].gold > self.players[1].gold else self.players[1]
        medalWinner = self.players[0] if self.players[0].medals > self.players[1].medals \
            else self.players[1]
        text = self.font.render(f"Winner Of Gold Is Player {gold_winner.num}"
                                f" With {gold_winner.gold} Gold", True, (0, 255, 255))
        self.screen.blit(text, (900, 400))

        text = self.font.render(f"Winner Of Medals Is Player {medalWinner.num}"
                                f" With {medalWinner.medals} Medals", True, (0, 255, 255))
        self.screen.blit(text, (900, 400))
        py.display.flip()

        if gold_winner == self.players[0] and medalWinner == self.players[0]:
            winner = self.players[0]
        elif gold_winner == self.players[1] and medalWinner == self.players[0]:
            winner = self.players[0]
        else:
            winner = self.players[1]
        self.reset_screen()
        time.sleep(2)
        text = self.font.render(f"The Winner Is Player Number {winner.num}", True, (0, 255, 255))
        self.screen.blit(text, (900, 400))
        py.display.flip()

        text = self.font.render("Game Is Over", True, (0, 255, 255))
        self.screen.blit(text, (900, 600))
        py.display.flip()
