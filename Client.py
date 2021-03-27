import pygame as py
from Network import Network as Net
from Player import Player
import random

REFRESH_RATE = 60


def clicked(event):
    return event.type == py.MOUSEBUTTONDOWN and event.button == 1


def main():
    p = Player()
    clock = py.time.Clock()
    net = Net()
    pos = net.get_pos()
    print(pos)
    p.connected = True
    player_num = int(pos[len(pos) - 1])
    current_player_num = player_num
    run = True
    did_not_start = True
    first_click = False
    num1 = random.randint(0, 1)
    while run:
        # try:
        clock.tick(REFRESH_RATE)
        game = net.send_obj(p)
        game.start()
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()

            elif game.ready and did_not_start:
                did_not_start = False
                game.main_menu()
            elif not game.ready:
                game.waiting_for_players_screen()
            elif game.ready and clicked(event) and not game.players_ready() is None and not first_click:
                game.reset_screen()
                game.choose_menu()
                first_click = True
            elif game.ready and clicked(event) and game.players[player_num].character is None and first_click \
                    and game.is_players_connected():
                p.character = game.choose_character(event)
            elif game.ready and game.players[player_num].character is not None and first_click \
                    and game.players[abs(player_num - 1)].character is None and game.is_players_connected():
                game.waiting_for_players_screen()
            elif game.ready and game.players_ready() and not game.start_game and game.is_players_connected():
                game.reset_screen()
                game.draw_field()
                for player in game.players:
                    player.character.x = 50
                    player.character.y = 210
                    player.currentTile = game.tiles[0]
                    game.draw_character(player.character)
                game.start_game = True
            if game.start_game and current_player_num == num1:
                if clicked(event):
                    game.main(game.players[current_player_num])
                    current_player_num = abs(num1 - 1)
    # except Exception as e:
    # print(e)
    # break
    print("Disconnected From The Server")


if __name__ == '__main__':
    main()
