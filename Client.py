import time

import pygame as py
from Network import Network as Net

REFRESH_RATE = 60


def clicked(event):
    return event.type == py.MOUSEBUTTONDOWN and event.button == 1


def main():
    clock = py.time.Clock()
    net = Net()
    try:
        game = net.get_game()
        game.initialize()
    except:
        print('Server Is Down')
        return
    my_p = net.send_str_get_obj('get')
    my_num = my_p.num
    print(f'You Are Player Number {my_num}')
    run = True
    msg = ''
    while run:
        try:
            for event in py.event.get():
                clock.tick(REFRESH_RATE)
                if event.type == py.QUIT:
                    run = False
                    py.quit()
                if game.start_button.clicked_on(event):
                    msg = f"{my_num} clicked start button"
                elif game.instructions_button.clicked_on(event):
                    msg = f"{my_num} clicked instructions button"
                elif game.return_button.clicked_on(event):
                    msg = f"{my_num} clicked return button"
                elif game.cube.clicked_on(event):
                    msg = f"{my_num} clicked on cube"
                elif clicked(event):
                    msg = f"{my_num} clicked"
                try:
                    to_do = net.recv_str()
                    if to_do == 'no':
                        pass
                    if to_do == "waiting for players screen":
                        game.waiting_for_players_screen()
                    if to_do == 'instructions':
                        game.instructions_screen(event)
                    if to_do == "main menu":
                        game.main_menu()
                    if to_do == "reset screen choose menu":
                        game.reset_screen()
                        game.choose_menu()
                    if to_do == "choose character":
                        try:
                            c = game.choose_character(event)
                            game.players[my_num].character = c
                            if c is not None:
                                msg = f'{my_num} chose {c}'
                        except:
                            pass
                    elif 'chose' in to_do:
                        if to_do.split('|')[1][:1] == '0':
                            name = to_do.split('|')[1][8:]
                            game.players[0].character = game.get_character_by_name(name)
                        else:
                            name = to_do.split('|')[1][8:]
                            game.players[1].character = game.get_character_by_name(name)
                    if 'not drawn' in to_do:
                        game.draw_field()
                        game.disp_player_num(my_num, True)
                        to_do = to_do.split("not drawn")[1]

                        num = int(to_do.split('|')[2])
                        num2 = int(to_do.split('|')[3])

                        game.players[0].path = game.paths[num]
                        game.players[1].path = game.paths[num2]

                        game.start_characters()
                        n = int(to_do.split('|')[1])
                        game.disp_player(n)
                        game.disp_player_num(my_num, True)
                    if "roll cube" in to_do:
                        to_do = to_do.split("|roll cube")[1]
                        num = int(to_do.split('|')[1])
                        game.cube.roll(game, num)

                        p_num = int(to_do.split("|")[2].split("-")[0])
                        p2_num = int(to_do.split("|")[2].split("-")[1])

                        p = game.players[p_num]
                        p2 = game.players[p2_num]
                        done = p.play(game, p2, num)
                        if done:
                            net.send_str(f'{my_num} finished')

                        n = int(to_do.split('|')[3])
                        game.disp_player(n)
                        game.disp_player_num(my_num, True)
                    elif 'finished' in to_do:
                        game.checkWinningPlayer()
                        game.reset_screen()
                        time.sleep(2)
                        game.print_to_screen('Game Is Over Closing The Game', (250, 400), False)
                        run = False
                    elif 'Player Disconnected' in to_do:
                        game.reset_screen()
                        game.print_to_screen('Other Player Disconnected, Closing The Game', (250, 400), False)
                        time.sleep(2)
                        run = False

                    if msg == '':
                        net.send_str('no')
                    else:
                        net.send_str(msg)
                    msg = ''
                except :
                    run = False
                    break

        except Exception as e:
            print(e)
            break
    print("Disconnected From The Server")
    net.send_str("Player Disconnected")


if __name__ == '__main__':
    main()
