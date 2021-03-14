import pygame as py
from Character import Character
from Tile import *
from Button import Button

root = 'D:\School\\2020-21\Cyber\Ofir\Work\Project\\Pictures\\'
start_img = root + 'start.png'
bill_img = root + 'bill.png'
dragon_img = root + 'dragon.png'
aatrox_img = root + 'aatrox.png'
map_img = root + 'map.png'


class Game:

    def __init__(self):
        self.width = 1700
        self.height = 900
        self.screen = None
        self.size = (self.width, self.height)
        self.clock = py.time.Clock()
        self.ready = False
        self.characters = None
        self.buttons = [Button(100, 700), Button(600, 700), Button(1150, 700)]
        self.tiles = []
        self.s = False

    def start(self):
        py.init()
        py.font.init()
        self.screen = py.display.set_mode((self.width, self.height))
        py.display.set_caption("Game")
        self.characters = [Character(bill_img, 150, 400), Character(dragon_img, 400, 350),
                           Character(aatrox_img, 1100, 300)]

    def clickedOnCharacter(self, event):
        characters = {100: self.characters[0], 600: self.characters[1], 1150: self.characters[2]}
        for btn in self.buttons:
            if btn.clickedOn(event):
                return characters[btn.x]

    def main(self):
        pass

    def reset_screen(self):
        self.screen.fill((0, 0, 0))

    def isReady(self):
        return self.ready

    def choose_menu(self):
        for character in self.characters:
            character.draw(self.screen)
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
        py.display.flip()

    def main_menu(self):
        self.screen.fill((255, 255, 255))
        img = py.image.load(start_img)
        self.screen.blit(img, (0, 0))
        py.display.flip()

    def waiting_for_players_Screen(self):
        self.reset_screen()
        font = py.font.SysFont("comicsans", 60)
        text = font.render("Waiting For Players...", True, (0, 255, 255))
        self.screen.blit(text, (600, 100))
        py.display.flip()
