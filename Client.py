import pygame as py
from Network import Network as Net
import time

REFRESH_RATE = 30


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
                elif game.ready and players_ready(my_p, other_p) and not game.start_game \
                        and is_players_connected(my_p, other_p):
                    if not drawn:
                        game.reset_screen()
                        game.draw_field()
                    for player in (my_p, other_p):
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
                    # elif game.roll_button.clicked_on(event) and other_p.num == game.current_player_num and n is not None:
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
