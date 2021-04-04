import pygame as py
from Network import Network as Net

REFRESH_RATE = 60


def clicked(event):
    return event.type == py.MOUSEBUTTONDOWN and event.button == 1


def is_players_connected(p1, p2):
    return p1.connected and p2.connected


def players_ready(p1, p2):
    return p1.character is not None and p2.character is not None


def main():
    clock = py.time.Clock()
    net = Net()
    game = net.get_game()
    game.initialize()
    my_p = net.send_str('get')
    player_num = my_p.num
    print(f'You Are Player Number {player_num}')
    run = True
    did_not_start = True
    first_click = False
    drawn = False
    while run:
        try:
            clock.tick(REFRESH_RATE)
            for event in py.event.get():
                other_p = net.send_obj(my_p)

                if event.type == py.QUIT:
                    run = False
                    py.quit()
                if is_players_connected(my_p, other_p):
                    game.ready = True

                if not game.ready:
                    game.waiting_for_players_screen()

                elif game.ready and did_not_start:
                    did_not_start = False
                    game.main_menu()
                    print("start")

                elif game.ready and game.start_button.clicked_on(event) \
                        and not players_ready(my_p, other_p) is None and not first_click:
                    game.reset_screen()
                    game.choose_menu()
                    first_click = True
                elif game.ready and clicked(event) and my_p.character is None and first_click \
                        and is_players_connected(my_p, other_p):
                    my_p.character = game.choose_character(event)
                elif game.ready and my_p.character is not None and first_click \
                        and other_p.character is None and is_players_connected(my_p, other_p):
                    game.waiting_for_players_screen()
                elif game.ready and players_ready(my_p, other_p) and not game.start_game and is_players_connected(my_p, other_p):
                    if not drawn:
                        game.reset_screen()
                        game.reset_screen()
                        game.draw_field()
                        game.player_turn(game.current_player_num, player_num)
                    # for player in game.players:
                    #    player.character.x = 50
                    #    player.character.y = 210
                    #    if not drawn:
                    #        game.draw_character(player.character)
                    #        player.currentTile = game.tiles[0]
                    drawn = True
                    game.start_game = True
                elif drawn and player_num == game.current_player_num:
                    my_p.turn = True
                    # if game.roll_button.clicked_on(event):
                    #    game.main(game.players[game.current_player_num])
        except Exception as e:
            print(e)
            break
    print("Disconnected From The Server")


if __name__ == '__main__':
    main()
