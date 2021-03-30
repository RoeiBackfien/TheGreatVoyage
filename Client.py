import pygame as py
from Network import Network as Net
from Player import Player
import random

REFRESH_RATE = 60


def clicked(event):
    return event.type == py.MOUSEBUTTONDOWN and event.button == 1


def main():
    clock = py.time.Clock()
    net = Net()
    p = net.get_p()
    player_num = p.num
    print(f'You Are Player Number {player_num}')
    p.connected = True
    run = True
    did_not_start = True
    first_click = False
    drawn = False
    while run:
        #try:
            clock.tick(REFRESH_RATE)
            game = net.send_obj(p)
            game.initialize()
            current_player = game.players[player_num]
            other_player = game.players[abs(player_num - 1)]
            for event in py.event.get():
                if event.type == py.QUIT:
                    run = False
                    py.quit()

                elif game.ready and did_not_start:
                    did_not_start = False
                    game.main_menu()
                elif not game.ready:
                    game.waiting_for_players_screen()
                elif game.ready and game.start_button.clicked_on(event) and not game.players_ready() is None and not first_click:
                    game.reset_screen()
                    game.choose_menu()
                    first_click = True
                elif game.ready and clicked(event) and current_player.character is None and first_click \
                        and game.is_players_connected():
                    p.character = game.choose_character(event)
                elif game.ready and current_player.character is not None and first_click \
                        and other_player.character is None and game.is_players_connected():
                    game.waiting_for_players_screen()
                elif game.ready and game.players_ready() and not game.start_game and game.is_players_connected():
                    if not drawn:
                        game.reset_screen()
                        game.reset_screen()
                        game.draw_field()
                        game.player_turn(game.current_player_num, player_num)
                    for player in game.players:
                        player.character.x = 50
                        player.character.y = 210
                        if not drawn:
                            game.draw_character(player.character)
                            player.currentTile = game.tiles[0]
                    drawn = True
                    game.start_game = True
                if drawn and player_num == game.current_player_num:
                    current_player.turn = True
                    if game.roll_button.clicked_on(event):
                        game.main(game.players[game.current_player_num])
        #except Exception as e:
        #    print(e)
        #    break
    print("Disconnected From The Server")


if __name__ == '__main__':
    main()
