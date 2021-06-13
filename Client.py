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
                    if to_do == 'no':
                        pass
                    if to_do == "waiting for players screen":
                        game.waiting_for_players_screen()
                    if to_do == "main menu":
                        game.main_menu()
                    if to_do == "reset screen choose menu":
                        game.reset_screen()
                        game.choose_menu()
                    if to_do == "choose character":
                        try:
                            game.players[my_p.num].character = cha[1]
                            msg = f'{my_p.num} chose {cha[1]}'
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
                        to_do = to_do.split("not drawn")[1]

                        num = int(to_do.split('|')[2])
                        num2 = int(to_do.split('|')[3])

                        game.players[0].path = game.paths[num]
                        game.players[1].path = game.paths[num2]

                        game.start_characters()
                        game.disp_player(int(to_do.split('|')[1]))
                    elif "roll cube" in to_do:
                        to_do = to_do.split("|roll cube")[1]
                        num = int(to_do.split('|')[1])
                        game.cube.roll(game, num)

                        p_num = int(to_do.split("|")[2].split("-")[0])
                        p2_num = int(to_do.split("|")[2].split("-")[1])

                        p = game.players[p_num]
                        p2 = game.players[p2_num]
                        done = p.play(game, p2, num)
                        if done:
                            net.send_str(f'{ p.num } finished')

                        game.disp_player(int(to_do.split('|')[3]))
                    elif 'finished' in to_do:
                        game.checkWinningPlayer()

                    if msg == '':
                        net.send_str('no')
                    else:
                        net.send_str(msg)
                    msg = ''
                except Exception as e:
                    print(e)
                    run = False
                    break

        except Exception as e:
            print(e)
            break
    print("Disconnected From The Server")
    net.send_str("Player Disconnected")


if __name__ == '__main__':
    main()
