import socket
import threading
import pickle
from Game import Game
from Player import Player
import random

IP = '192.168.1.2'
PORT = 5555
ADDR = (IP, PORT)


def generate_random_player_turn():
    return random.randint(0, 1)


def handle_client(conn, addr, player_num, game):
    game.players[player_num].num = player_num
    game.players[player_num].connected = True
    conn.send(pickle.dumps(game))
    data = ''
    while True:
        try:
            data = conn.recv(2048)
            pickled_data = pickle.loads(data)
            if not pickled_data:
                break
            game.players[player_num] = pickled_data
            if player_num == 1:
                game.ready = True
                p = game.players[0]
            else:
                p = game.players[1]
            conn.send(pickle.dumps(p))
        except:
            try:
                str_data = data.decode()
                if not str_data:
                    break
                elif str_data == 'get':
                    conn.send(pickle.dumps(game.players[player_num]))
                elif str_data == 'n':
                    pass
            except:
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
    player_turn = generate_random_player_turn()
    while True:
        if currentPlayer % 2 == 0:
            game = Game(game_id)
            game_id += 1
            game.current_player_num = player_turn
            currentPlayer = 0
        conn, addr = s.accept()
        print(addr, 'Is Connected To The Server')
        threading.Thread(target=handle_client, args=(conn, addr, currentPlayer, game)).start()
        currentPlayer += 1


if __name__ == '__main__':
    main()
