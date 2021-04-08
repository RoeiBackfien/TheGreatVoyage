import pygame as py
from Character import Character
from Tile import *
from Button import Button
from Player import Player
from Cube import Cube
import time
import random

root = 'D:\School\\2020-21\Cyber\Ofir\Work\TheGreatVoyage\\Pictures\\'
start_img = root + 'start.png'
bill_img = root + 'bill.png'
dragon_img = root + 'dragon.png'
aatrox_img = root + 'aatrox.png'
small_aatrox_img = root + 'small aatrox.png'
small_bill_img = root + 'small bill.png'
small_dragon_img = root + 'small dragon.png'
map_img = root + 'map.png'


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
                              FateMaskTile(360, 522), LoseGoldTile(470, 522)]
        self.first_split_2 = [GoldTile(250, 210), FreezeTile(330, 270), FateMaskTile(420, 335), LoseGoldTile(510, 410)]
        self.mid_tiles = [ReverseTile(570, 522), LoseGoldTile(680, 522), FreezeTile(780, 522)]
        self.second_split_1 = []
        self.second_split_2 = []
        self.end_tiles = [FreezeTile(1400, 320), GoldTile(1500, 320), ReverseTile(1600, 320)]
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
                return characters[btn.x]

    def main(self, player, player2, num):
        # text = self.font.render(str(num), True, (0, 255, 255))
        # self.screen.blit(text, (400, 20))
        # py.display.flip()
        if player.turn:
            p = player
            p2 = player2
        else:
            p = player2
            p2 = player
        x, y = p.play(self.tiles, num)
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
                self.draw_character(other_character)
                time.sleep(1)
        elif x_diff == 0:
            while y != des_y:
                self.draw_field()
                y += y_diff
                character.y = y
                self.draw_character(character)
                self.draw_character(other_character)
                time.sleep(1)
        elif y_diff == 0:
            while x != des_x:
                self.draw_field()
                x += x_diff
                character.x = x
                self.draw_character(character)
                self.draw_character(other_character)
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
        for button in self.characters_buttons:
            button.draw(self.screen)
        text = self.font.render("Choose Your Champion", True, (0, 255, 255))
        self.screen.blit(text, (600, 100))
        py.display.flip()

    def draw_field(self):
        img = py.image.load(map_img).convert()
        img.set_colorkey((255, 255, 255))
        self.screen.blit(img, (0, 0))
        py.draw.rect(self.screen, (153, 76, 0), (0, 0, 1700, 100))
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
