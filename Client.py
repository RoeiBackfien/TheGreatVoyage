import pygame as py
from Network import Network as Net
import threading

REFRESH_RATE = 60


def clicked(event):
    return event.type == py.MOUSEBUTTONDOWN and event.button == 1


def main():
    clock = py.time.Clock()
    net = Net()
    game = net.get_game()
    game.initialize()
    my_p = net.send_str_get_obj('get')
    print(f'You Are Player Number {my_p.num}')
    run = True
    cha = ''
    msg = ''
    while run:
        try:
            for event in py.event.get():
                clock.tick(REFRESH_RATE)
                if event.type == py.QUIT:
                    run = False
                    py.quit()
                if game.start_button.clicked_on(event):
                    msg = f"{my_p.num} clicked start button"
                elif game.cube.clicked_on(event):
                    msg = f"{my_p.num} clicked on cube"
                elif clicked(event):
                    cha = game.choose_character(event)
                    try:
                        if cha[0]:
                            msg = f"{my_p.num} clicked on character"
                        else:
                            msg = f"{my_p.num} clicked"
                    except:
                        pass
                try:
                    to_do = net.recv_str()
                except:
                    break
                if to_do == 'no':
                    pass
                elif to_do == "waiting for players screen":
                    game.waiting_for_players_screen()
                elif to_do == "main menu":
                    game.main_menu()
                    print(to_do)
                elif to_do == "reset screen choose menu":
                    print(to_do)
                    game.reset_screen()
                    game.choose_menu()
                elif "choose character" in to_do:
                    try:
                        game.players[my_p.num].character = cha[1]
                        msg = f'{my_p.num} chose {cha[1]}'
                        print(msg)
                        print(cha[1])
                    except:
                        pass
                elif to_do == "disp player turn":
                    game.disp_player_turn(game.current_player_num, my_p.num)
                    print(to_do)
                elif to_do.split(",")[0][:len(to_do) - 1] == "roll cube main":
                    print(to_do)
                    num = to_do[len(to_do) - 1:]
                    game.cube.roll(game, num)
                    p = game.players[to_do.split(",")[1].split("-")[0]]
                    p2 = game.players[to_do.split(",")[1].split("-")[1]]
                    game.main(p, p2, num)
                elif to_do == "not drawn":
                    print(to_do)
                    game.draw_field()
                    game.start_characters()
                if msg == '':
                    net.send_str('no')
                else:
                    net.send_str(msg)
                msg = ''

        except Exception as e:
            print(e)
            break
    print("Disconnected From The Server")
    net.send_str("Player Disconnected")


if __name__ == '__main__':
    main()
