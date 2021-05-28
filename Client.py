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
    while run:
        try:
            for event in py.event.get():
                clock.tick(REFRESH_RATE)
                if event.type == py.QUIT:
                    run = False
                    py.quit()
                if game.start_button.clicked_on(event):
                    net.send_str(f"{my_p.num} clicked start button")
                elif game.cube.clicked_on(event):
                    net.send_str(f"{my_p.num} clicked on cube")
                elif clicked(event):
                    cha = game.choose_character(event)
                    if cha[0]:
                        net.send_str(f'{my_p.num} clicked on character')
                    else:
                        net.send_str(f"{my_p.num} clicked")
                else:
                    net.send_str('no')
                try:
                    to_do = net.recv_str()
                    print(to_do)
                except:
                    break
                if to_do == 'no':
                    pass
                elif to_do == "waiting for players screen":
                    game.waiting_for_players_screen()
                elif to_do == "main menu":
                    game.main_menu()
                    print(to_do)
                elif "choose character" in to_do:
                    game.players[my_p.num].character = cha[1]
                    print(to_do)
                elif to_do == "disp player turn":
                    game.disp_player_turn(game.current_player_num, my_p.num)
                    print(to_do)
                elif to_do.split(",")[0][:len(to_do) - 1] == "roll cube main":
                    print(to_do)
                    roll_num = game.cube.roll(game, to_do[len(to_do) - 1:])
                    p = game.players[to_do.split(",")[1].split("-")[0]]
                    p2 = game.players[to_do.split(",")[1].split("-")[1]]
                    game.main(p, p2, roll_num)
                elif to_do == "reset screen choose menu":
                    print(to_do)
                    game.reset_screen()
                    game.choose_menu()
                elif to_do == "not drawn":
                    print(to_do)
                    game.draw_field()
                    for player in game.players:
                        player.character.x = 50
                        player.character.y = 210
                        game.draw_character(player.character)
                        player.currentTile = game.tiles[0]
        except Exception as e:
            print(e)
            break
    print("Disconnected From The Server")
    net.send_str("Player Disconnected")


if __name__ == '__main__':
    threading.Thread(target=main, args=()).start()
