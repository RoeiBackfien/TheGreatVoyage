import pygame as py
from Network import Network as Net

REFRESH_RATE = 60


def clicked(event):
    return event.type == py.MOUSEBUTTONDOWN and event.button == 1


def main():
    clock = py.time.Clock()
    net = Net()
    game = net.get_game()
    game.initialize()
    my_p = net.send_str('get')
    print(f'You Are Player Number {my_p.num}')
    run = True
    did_not_start = True
    first_click = False
    drawn = False
    while run:
        try:
            clock.tick(REFRESH_RATE)
            for event in py.event.get():
                other_p = net.send_obj(my_p)
                game.players[my_p.num] = my_p
                game.players[other_p.num] = other_p

                if event.type == py.QUIT:
                    run = False
                    py.quit()
                if game.is_players_connected():
                    game.ready = True

                if not game.ready:
                    game.waiting_for_players_screen()

                elif game.ready and did_not_start:
                    did_not_start = False
                    game.main_menu()

                elif game.ready and game.start_button.clicked_on(event) \
                        and not game.players_ready() is None and not first_click:
                    game.reset_screen()
                    game.choose_menu()
                    first_click = True
                elif game.ready and clicked(event) and my_p.character is None and first_click \
                        and game.is_players_connected():
                    my_p.character = game.choose_character(event)
                elif game.ready and my_p.character is not None and first_click \
                        and other_p.character is None and game.is_players_connected():
                    game.waiting_for_players_screen()
                elif game.ready and game.players_ready() and not game.start_game \
                        and game.is_players_connected():
                    if not drawn:
                        game.draw_field()
                    for player in game.players:
                        player.character.x = 50
                        player.character.y = 210
                        if not drawn:
                            game.draw_character(player.character)
                            player.currentTile = game.tiles[0]
                    drawn = True
                    game.start_game = True
                elif drawn:
                    game.disp_player_turn(game.current_player_num, my_p.num)
                    if my_p.num == game.current_player_num:
                        my_p.turn = True
                        p = my_p
                        p2 = other_p
                    else:
                        other_p.turn = True
                        p = other_p
                        p2 = my_p
                    if game.cube.clicked_on(event) and my_p.num == game.current_player_num:
                        roll_num = game.cube.roll(game)
                        game.main(p, p2, roll_num)
                        if p.turn:
                            p.turn = False
                            p2.turn = True
                        game.current_player_num = abs(p.num - 1)
                    # elif game.roll_button.clicked_on(event) and other_p.num == game.current_player_num:
                    #    game.main(p2, p, roll_num)
                    #    if p.turn:
                    #        p.turn = False
                    #        p2.turn = True
                    #        game.current_player_num = abs(p.num - 1)

        except Exception as e:
            print(e)
            break
    print("Disconnected From The Server")


if __name__ == '__main__':
    main()
