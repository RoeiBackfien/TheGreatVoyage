import pygame as py
from Character import Character
from Tile import *
from Button import Button
from Player import Player
from Cube import Cube
import time

root = 'D:\School\\2020-21\Cyber\Ofir\Work\TheGreatVoyage\\Pictures\\'
end = '.png'
start_img = root + 'start' + end
bill_img = root + 'bill' + end
dragon_img = root + 'dragon' + end
aatrox_img = root + 'aatrox' + end
small_aatrox_img = root + 'small aatrox' + end
small_bill_img = root + 'small bill' + end
small_dragon_img = root + 'small dragon' + end
map_img = root + 'map' + end
gold_img = root + 'gold' + end
medal_img = root + 'medal' + end


class Game:

    def __init__(self, id):
        self.id = id
        self.width = 1700
        self.height = 900
        self.size = (self.width, self.height)
        self.screen = None
        self.font = None
        self.ready = False
        self.characters = None
        self.characters_buttons = [Button(100, 700, 300, 100, (200, 150, 150), 'Choose'),
                                   Button(600, 700, 300, 100, (200, 150, 150), 'Choose'),
                                   Button(1150, 700, 300, 100, (200, 150, 150), 'Choose')]
        self.start_button = Button(600, 700, 300, 100, (200, 150, 150), 'Start')
        self.instructions_button = Button(600, 700, 300, 100, (200, 150, 150), 'Instructions')
        self.start_tiles = [GoldTile(50, 210), LoseGoldTile(150, 210)]
        self.first_split_1 = [FreezeTile(150, 320), ReverseTile(150, 420), GoldTile(150, 520), LoseGoldTile(250, 522),
                              ReverseTile(360, 522), LoseGoldTile(470, 522)]
        self.first_split_2 = [GoldTile(250, 210), FreezeTile(330, 270), AnotherTurnTile(420, 335),
                              LoseGoldTile(510, 410)]
        self.mid_tiles = [ReverseTile(570, 522), LoseGoldTile(680, 522), FreezeTile(780, 522)]
        self.second_split_1 = [GoldTile(720, 610), LoseGoldTile(640, 650), FreezeTile(550, 660), LoseGoldTile(450, 660),
                               GoldTile(350, 660), LoseGoldTile(250, 660), ReverseTile(160, 700), GoldTile(170, 790),
                               FreezeTile(270, 810), LoseGoldTile(370, 815), GoldTile(470, 815), ReverseTile(600, 815),
                               GoldTile(700, 815), GoldTile(800, 815), MedalTile(900, 815), GoldTile(1000, 815),
                               GoldTile(1100, 815), GoldTile(1200, 815), GoldTile(1300, 815), LoseGoldTile(1380, 740),
                               LoseGoldTile(1380, 640), LoseGoldTile(1380, 540), LoseGoldTile(1380, 440)]
        self.second_split_2 = [GoldTile(880, 522), LoseGoldTile(850, 440), FreezeTile(795, 370), GoldTile(750, 290),
                               LoseGoldTile(710, 200), GoldTile(810, 180), FreezeTile(910, 180), ReverseTile(1100, 180),
                               GoldTile(1200, 180), FreezeTile(1300, 180), ReverseTile(1380, 180), GoldTile(1380, 260)]
        self.end_tiles = [FreezeTile(1380, 340), GoldTile(1480, 340), ReverseTile(1580, 340)]
        self.tiles = self.start_tiles + self.first_split_1 + self.first_split_2 \
                     + self.mid_tiles + self.second_split_1 + self.second_split_2 + self.end_tiles
        self.cube = Cube(0, 0, (255, 50, 0))
        self.start_game = False
        self.current_player_num = -1
        self.players = [Player(), Player()]

    def initialize(self):
        py.init()
        py.font.init()
        self.font = pygame.font.SysFont("comicsans", 60)
        self.screen = py.display.set_mode(self.size)
        py.display.set_caption("Game")
        self.characters = [Character(small_bill_img, 150, 400, 'bill'), Character(small_dragon_img, 400, 350, 'dragon'),
                           Character(small_aatrox_img, 1100, 300, 'aatrox')]

    def choose_character(self, event):
        characters = {self.characters_buttons[0].x: self.characters[0],
                      self.characters_buttons[1].x: self.characters[1],
                      self.characters_buttons[2].x: self.characters[2]}
        for btn in self.characters_buttons:
            if btn.clicked_on(event):
                return True, characters[btn.x]

    def main(self, player, player2, num):
        if player.turn:
            p = player
            p2 = player2
        else:
            p = player2
            p2 = player
        print(num)
        for i in range(num):
            x, y = p.play(self.tiles)
            self.move_character(p.character, x, y, p2.character)
        p.update()

    def disp_player_turn(self, player_num_turn, current_player_num):
        if player_num_turn == current_player_num:
            t = 'Your Turn'
        else:
            t = 'Enemy Turn'
        text = self.font.render(t, True, (0, 255, 255))
        self.screen.blit(text, (300, 20))
        py.display.flip()

    def move_character(self, character, des_x, des_y, other_character):
        x = character.x
        y = character.y
        y_diff = (des_y - y) / 2
        x_diff = (des_x - x) / 2
        if x_diff != 0 and y_diff != 0:
            while x != des_x and y != des_y:
                self.draw_field()
                x += x_diff
                y += y_diff
                character.x = x
                character.y = y
                self.draw_character(character)
                self.draw_character(other_character)
                time.sleep(0.4)
        elif x_diff == 0:
            while y != des_y:
                self.draw_field()
                y += y_diff
                character.y = y
                self.draw_character(character)
                self.draw_character(other_character)
                time.sleep(0.4)
        elif y_diff == 0:
            while x != des_x:
                self.draw_field()
                x += x_diff
                character.x = x
                self.draw_character(character)
                self.draw_character(other_character)
                time.sleep(0.4)

    def reset_screen(self):
        self.screen.fill((0, 0, 0))

    def is_players_connected(self):
        return self.players[0].connected and self.players[1].connected

    def players_ready(self):
        return self.players[0].character is not None and self.players[1].character is not None

    def draw_character(self, character):
        img = py.image.load(character.img).convert()
        img.set_colorkey((255, 255, 255))
        self.screen.blit(img, (character.x, character.y))
        py.display.flip()

    def choose_menu(self):
        for character in self.characters:
            self.draw_character(character)
        for button in self.characters_buttons:
            button.draw(self.screen)
        text = self.font.render("Choose Your Champion", True, (0, 255, 255))
        self.screen.blit(text, (600, 100))
        py.display.flip()

    def draw_field(self, player=None):
        img = py.image.load(map_img).convert()
        img.set_colorkey((255, 255, 255))
        self.screen.blit(img, (0, 0))
        py.draw.rect(self.screen, (153, 76, 0), (0, 0, 1700, 120))
        if player is not None:
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
        for tile in self.tiles:
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
        self.screen.blit(text, (200, 20))
        text = self.font.render(f"Winner Of Medals Is Player {medalWinner.num}"
                                f" With {medalWinner.medals} Medals", True, (0, 255, 255))
        self.screen.blit(text, (200, 60))
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
        self.screen.blit(text, (200, 60))
        py.display.flip()
