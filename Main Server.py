import socket
import threading
import pickle
from Game import Game
from Player import Player
import random

IP = '192.168.1.2'
PORT = 5555
ADDR = (IP, PORT)

players = [Player(), Player()]


def generate_random_player_turn():
    return random.randint(0, 1)


def handle_client(conn, addr, player_num, game):
    players[player_num].num = player_num
    players[player_num].connected = True
    print(player_num, players[player_num].connected)
    conn.send(pickle.dumps(game))
    data = ''
    while True:
        print(players[0].connected)
        try:
            data = conn.recv(2048)
            pickled_data = pickle.loads(data)
            if not pickled_data:
                break
            players[player_num] = pickled_data

        except Exception as e:
            print(e)
            try:
                str_data = data.decode()
                if not str_data:
                    break
                elif str_data == 'get':
                    conn.send(pickle.dumps(players[player_num]))
            except Exception as e:
                print(e)
                break
        if player_num == 1:
            game.ready = True
            p = players[0]
        else:
            p = players[1]
        conn.sendall(pickle.dumps(p))

        if players[player_num].turn:
            players[player_num].turn = False
            players[abs(player_num - 1)].turn = True
            game.current_player_num = players[abs(player_num - 1)]

    print(addr, 'Disconnected From The Server')
    players[player_num].connected = False
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
            currentPlayer = 0
        conn, addr = s.accept()
        print(addr, 'Is Connected To The Server')
        player_turn = generate_random_player_turn()
        game.current_player_num = player_turn
        threading.Thread(target=handle_client, args=(conn, addr, currentPlayer, game)).start()
        currentPlayer += 1


if __name__ == '__main__':
    main()
