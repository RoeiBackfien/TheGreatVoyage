import pygame as py
from Character import Character
from Tile import *
from Button import Button
from Player import Player
from Cube import Cube
import time

root = 'D:\School\\2020-21\Cyber\Ofir\Work\TheGreatVoyage\\Pictures\\'
start_img = root + 'start.png'
bill_img = root + 'bill.png'
dragon_img = root + 'dragon.png'
aatrox_img = root + 'aatrox.png'
small_aatrox_img = root + 'small aatrox.png'
map_img = root + 's.png'


class Game:

    def __init__(self, id):
        self.id = id
        self.width = 1700
        self.height = 900
        self.size = (self.width, self.height)
        self.screen = None
        self.ready = False
        self.characters = None
        self.buttons = [Button(100, 700), Button(600, 700), Button(1150, 700)]
        self.start_tiles = [GoldTile(50, 210), LoseGoldTile(150, 210)]
        self.first_split_1 = [FreezeTile(150, 320), ReverseTile(150, 420), GoldTile(150, 520), LoseGoldTile(250, 522),
                              FateMaskTile(360, 522), LoseGoldTile(470, 522)]
        self.first_split_2 = [GoldTile(250, 210), FreezeTile(330, 270), FateMaskTile(420, 335), LoseGoldTile(510, 410)]
        self.mid_tiles = [ReverseTile(570, 522), LoseGoldTile(680, 522), FreezeTile(780, 522)]
        self.second_split_1 = []
        self.second_split_2 = []
        self.end_tiles = [FreezeTile(1400, 320), GoldTile(1500, 320), ReverseTile(1600, 320)]
        self.tiles = self.start_tiles + self.first_split_1 + self.first_split_2 \
                     + self.mid_tiles + self.second_split_1 + self.second_split_2 + self.end_tiles
        self.players = [Player(), Player()]
        self.cube = Cube()
        self.start_game = False

    def start(self):
        py.init()
        py.font.init()
        self.screen = py.display.set_mode(self.size)
        py.display.set_caption("Game")
        self.characters = [Character(bill_img, 150, 400, 'bill'), Character(dragon_img, 400, 350, 'dragon'),
                           Character(small_aatrox_img, 1100, 300, 'aatrox')]

    def is_players_connected(self):
        for p in self.players:
            if p.connected is False:
                return False
        return True

    def choose_character(self, event):
        characters = {self.buttons[0].x: self.characters[0], self.buttons[1].x: self.characters[1],
                      self.buttons[2].x: self.characters[2]}
        for btn in self.buttons:
            if btn.clicked_on(event):
                return characters[btn.x]

    def players_ready(self):
        for p in self.players:
            if p.character is None:
                return False
        return True

    def main(self, player):
        player.turn = True
        x, y = player.play(self.tiles, 2)
        self.move_character(player.character, x, y)
        player.turn = False

    def move_character(self, character, des_x, des_y):
        x = character.x
        y = character.y
        y_diff = (des_y - y) / 4
        x_diff = (des_x - x) / 4
        if x_diff != 0 and y_diff != 0:
            while x != des_x and y != des_y:
                self.draw_field()
                x += x_diff
                y += y_diff
                character.x = x
                character.y = y
                self.draw_character(character)
                time.sleep(1)
        elif x_diff == 0:
            while y != des_y:
                self.draw_field()
                y += y_diff
                character.y = y
                self.draw_character(character)
                time.sleep(1)
        elif y_diff == 0:
            while x != des_x:
                self.draw_field()
                x += x_diff
                character.x = x
                self.draw_character(character)
                time.sleep(1)

    def reset_screen(self):
        self.screen.fill((0, 0, 0))

    def draw_character(self, character):
        img = py.image.load(character.img).convert()
        img.set_colorkey((255, 255, 255))
        self.screen.blit(img, (character.x, character.y))
        py.display.flip()

    def choose_menu(self):
        for character in self.characters:
            self.draw_character(character)
        for button in self.buttons:
            button.draw(self.screen)
        font = py.font.SysFont("comicsans", 60)
        text = font.render("Choose Your Champion", True, (0, 255, 255))
        self.screen.blit(text, (600, 100))
        py.display.flip()

    def draw_field(self):
        img = py.image.load(map_img).convert()
        img.set_colorkey((255, 255, 255))
        self.screen.blit(img, (0, 0))
        py.draw.rect(self.screen, (153, 76, 0), (0, 0, 1700, 100))
        for tile in self.tiles:
            tile.draw(self.screen)
        py.display.flip()

    def main_menu(self):
        self.reset_screen()
        img = py.image.load(start_img)
        self.screen.blit(img, (0, 0))
        py.display.flip()

    def waiting_for_players_screen(self):
        self.reset_screen()
        font = py.font.SysFont("comicsans", 60)
        text = font.render("Waiting For Players...", True, (0, 255, 255))
        self.screen.blit(text, (600, 100))
        py.display.flip()
