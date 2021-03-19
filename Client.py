import pygame as py
from Network import Network as Net
from Player import Player

REFRESH_RATE = 60


def clicked(event):
    return event.type == py.MOUSEBUTTONDOWN and event.button == 1


def main():
    clock = py.time.Clock()
    net = Net()
    pos = net.get_pos()
    print(pos)
    player_num = int(pos[len(pos) - 1])
    p = Player()
    run = True
    did_not_start = True
    first_click = False
    drawn = False
    while run:
        try:
            clock.tick(REFRESH_RATE)
            game = net.send(p)
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
                elif game.ready and clicked(event) and game.players[player_num].character is None and first_click:
                    p.character = game.choose_character(event)
                elif game.ready and game.players[player_num].character is not None and first_click \
                        and game.players[abs(player_num - 1)].character is None:
                    game.waiting_for_players_screen()
                elif game.ready and game.players_ready():
                    game.reset_screen()
                    game.draw_field()
                    if not drawn:
                        for player in game.players:
                            game.draw_character(player.character)
                        drawn = True
        except:
            break
    print("Disconnected From The Server")


if __name__ == '__main__':
    main()
