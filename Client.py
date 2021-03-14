import pygame as py
from Network import Network as Net
from Game import Game
from Player import Player
from Character import Character

REFRESH_RATE = 60


def clicked(event):
    return event.type == py.MOUSEBUTTONDOWN and event.button == 1


def main():
    clock = py.time.Clock()
    net = Net()
    print(net.get_pos())
    run = True
    game = Game()
    game.start()
    p = Player()
    did_not_start = True
    first_click = False
    while run:
        clock.tick(REFRESH_RATE)
        isReady = net.send("get").decode()
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()
            elif isReady == 'True' and did_not_start:
                did_not_start = False
                game.main_menu()
            elif not (isReady == 'True'):
                game.waiting_for_players_Screen()
            elif isReady == 'True' and clicked(event) and p.character is None and not first_click:
                game.reset_screen()
                game.choose_menu()
                first_click = True
            elif isReady == 'True' and clicked(event) and p.character is None and first_click:
                p.character = game.clickedOnCharacter(event)
                print(p.character)
            elif isReady == 'True' and not (p.character is None):
                game.reset_screen()
                game.draw_field()


if __name__ == '__main__':
    main()
