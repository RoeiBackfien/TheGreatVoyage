import socket
import threading
import pickle
from Game import Game
import random

IP = '0.0.0.0'
PORT = 5555
ADDR = (IP, PORT)


def generate_random_player_turn():
    return random.randint(0, 1)


def generate_random_cube_roll():
    return random.randint(1, 6)


def handle_client(conn, addr, player_num, game):
    game.players[player_num].num = player_num
    game.players[player_num].connected = True
    conn.send(pickle.dumps(game))
    data = ''
    did_not_start = True
    first_click = False
    drawn = False
    clicked = ''
    while True:
        try:
            if player_num == 1:
                game.ready = True
            data = conn.recv(2048)
            pickled_data = pickle.loads(data)
            if not pickled_data:
                break
            game.players[player_num] = pickled_data
        except:
            try:
                str_data = data.decode()
                if not str_data:
                    break
                elif str_data == 'get':
                    conn.send(pickle.dumps(game.players[player_num]))
                elif str_data[2:] == 'clicked':
                    if str_data[:2]:
                        clicked = "0 clicked"
                    else:
                        clicked = "1 clicked"
                    print(clicked)
                elif str_data[2:] == "clicked start button":
                    if str_data[:1] == '0':
                        clicked = "0 clicked start button"
                    else:
                        clicked = "1 clicked start button"
                    print(clicked)
                elif str_data[2:] == "clicked on cube":
                    if str_data[:1] == '0':
                        clicked = "0 clicked on cube"
                    else:
                        clicked = "1 clicked on cube"
                    print(clicked)
                elif str_data[2:] == 'clicked on character':
                    if str_data[:1] == '0':
                        clicked = "0 clicked on character"
                    else:
                        clicked = "1 clicked on character"
                    print(clicked)
                elif str_data[2:7] == 'chose':
                    if str_data[:1] == '0':
                        game.players[0].character = str_data[8:]
                        print(f'0 chose {str_data[8:]}')
                    else:
                        game.players[1].character = str_data[8:]
                        print(f'1 chose {str_data[8:]}')
            except:
                pass
        my_p = game.players[player_num]
        other_p = game.players[abs(player_num - 1)]
        try:
            if not game.ready:
                conn.send("waiting for players screen".encode())

            elif game.ready and did_not_start:
                did_not_start = False
                conn.sendall("main menu".encode())

            elif game.ready and clicked == f'{player_num} clicked start button'  \
                    and not game.players_ready() is None and not first_click:
                conn.send("reset screen choose menu".encode())
                first_click = True
            elif game.ready and my_p.character is None and first_click and game.is_players_connected():
                conn.send("choose character".encode())
            elif game.ready and my_p.character is not None and first_click \
                    and other_p.character is None and game.is_players_connected():
                conn.send("waiting for players screen".encode())
            elif game.ready and game.players_ready() and not game.start_game \
                    and game.is_players_connected():
                print(game.players[0].character)
                print(game.players[1].character)
                if not drawn:
                    conn.send("not drawn".encode())
                drawn = True
                game.start_game = True
            elif drawn:
                conn.send("disp player turn".encode())
                if my_p.num == game.current_player_num:
                    my_p.turn = True
                    p = my_p
                    p2 = other_p
                else:
                    other_p.turn = True
                    p = other_p
                    p2 = my_p
                if clicked == f'{player_num} clicked on cube':
                    conn.sendall(f"roll cube main {generate_random_cube_roll()}, {p.num}-{p2.num}".encode())
                    if p.turn:
                        p.turn = False
                        p2.turn = True
                    game.current_player_num = abs(p.num - 1)
            else:
                conn.send('no'.encode())
        except Exception as e:
            print(e)
            break

    print(addr, 'Disconnected From The Server')
    game.players[player_num].connected = False
    conn.close()


def main():
    currentPlayer = 0
    game_id = 0
    game = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ADDR)
    s.listen()
    print('Server Is Up')
    while True:
        if currentPlayer % 2 == 0:
            game = Game(game_id)
            game_id += 1
            game.current_player_num = generate_random_player_turn()
            currentPlayer = 0
        try:
            conn, addr = s.accept()
            print(addr, 'Is Connected To The Server')
            threading.Thread(target=handle_client, args=(conn, addr, currentPlayer, game)).start()
            currentPlayer += 1
        except Exception as e:
            print(e)
            break


if __name__ == '__main__':
    main()
