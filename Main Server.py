import socket
import threading
import pickle
from Game import Game
import random

IP = '0.0.0.0'
PORT = 5555
ADDR = (IP, PORT)
CONNECTIONS = []


def generate_random_player_turn():
    return random.randint(0, 1)


def generate_random_cube_roll():
    return random.randint(1, 6)


def generate_path_num():
    return random.randint(0, 3)


def handle_client(conn, addr, player_num, game, game_id):
    global CONNECTIONS
    game.players[player_num].num = player_num
    game.players[player_num].connected = True
    conn.send(pickle.dumps(game))
    data = ''
    did_not_start = True
    first_click = False
    drawn = False
    clicked = ''
    msg = ''
    reset = False
    while True:
        try:
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

                elif str_data[2:] == "clicked start button":
                    if str_data[:1] == '0':
                        clicked = "0 clicked start button"
                    else:
                        clicked = "1 clicked start button"

                elif str_data[2:] == "clicked instructions button":
                    if str_data[:1] == '0':
                        clicked = "0 clicked instructions button"
                    else:
                        clicked = "1 clicked instructions button"

                elif str_data[2:] == "clicked return button":
                    if str_data[:1] == '0':
                        clicked = "0 clicked return button"
                    else:
                        clicked = "1 clicked return button"

                elif str_data[2:] == "clicked on cube":
                    if str_data[:1] == '0':
                        clicked = "0 clicked on cube"
                    else:
                        clicked = "1 clicked on cube"

                elif str_data[2:] == 'clicked on character':
                    if str_data[:1] == '0':
                        clicked = "0 clicked on character"
                    else:
                        clicked = "1 clicked on character"

                elif str_data[2:7] == 'chose':
                    if str_data[:1] == '0':
                        game.players[0].character = str_data[8:]
                    else:
                        game.players[1].character = str_data[8:]
                    msg = f'|{player_num} chose {str_data[8:]}|'
                elif 'finished' in str_data:
                    msg = 'finished'
            except:
                pass
        current_p = game.players[player_num]
        other_p = game.players[abs(player_num - 1)]
        try:
            if did_not_start:
                if msg == '':
                    did_not_start = False
                    msg = "main menu"

            elif clicked == f'{player_num} clicked instructions button':
                if msg == '':
                    msg = "instructions"

            elif clicked == f'{player_num} clicked return button':
                msg = "main menu"

            elif clicked == f'{player_num} clicked start button' and not first_click:
                if msg == '':
                    msg = "waiting for players screen"
                    first_click = True
            elif game.is_players_connected() and current_p.character is None and first_click and not reset:
                if msg == '':
                    msg = 'reset screen choose menu'
                    reset = True
            elif game.is_players_connected() and current_p.character is None and first_click and reset:
                if msg == '':
                    msg = "choose character"
            elif game.is_players_connected() and current_p.character is not None and first_click and other_p.character is None:
                if msg == '':
                    msg = "waiting for players screen"
            elif game.is_players_connected() and game.players_ready() and not drawn and msg == '':
                msg = f"not drawn|{game.current_player_num}|{generate_path_num()}|{generate_path_num()}"
                drawn = True

            elif game.is_players_connected() and drawn and clicked == f'{player_num} clicked on cube' and \
                    player_num == game.current_player_num:
                game.current_player_num = abs(game.current_player_num - 1)
                msg = f"|roll cube|{generate_random_cube_roll()}" \
                      f"|{current_p.num}-{other_p.num}|{game.current_player_num}"
            else:
                if msg == '':
                    msg = 'no'
            if 'roll' in msg or msg[3:8] == 'chose' or msg[:9] == 'not drawn' or msg == 'finished':
                CONNECTIONS[game_id * 2].send(msg.encode())
                CONNECTIONS[game_id * 2 + 1].send(msg.encode())
            else:
                conn.send(msg.encode())
            msg = ''
            clicked = ''
        except:
            break

    print(addr, 'Disconnected From The Server')
    game.players[player_num].connected = False
    try:
        CONNECTIONS[abs(player_num - 1)].send("Player Disconnected".encode())
        CONNECTIONS.remove(conn)
        conn.close()
    except:
        conn.close()


def main():
    currentPlayer = 0
    game_id = -1
    game = None
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ADDR)
    s.listen()
    print('Server Is Up')
    while True:
        if currentPlayer % 2 == 0:
            game_id += 1
            game = Game(game_id)
            game.current_player_num = generate_random_player_turn()
            currentPlayer = 0
        try:
            conn, addr = s.accept()
            CONNECTIONS.append(conn)
            print(addr, 'Is Connected To The Server')
            threading.Thread(target=handle_client, args=(conn, addr, currentPlayer, game, game_id)).start()
            currentPlayer += 1
        except:
            break


if __name__ == '__main__':
    main()
