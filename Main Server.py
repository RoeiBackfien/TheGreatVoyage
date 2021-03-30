import socket
import threading
import pickle
from Game import Game
import random

IP = '192.168.1.2'
PORT = 5555
ADDR = (IP, PORT)


def generate_random_player_turn():
    return random.randint(0, 1)


def handle_client(conn, addr, player_num, game):
    game.players[player_num].num = player_num
    conn.send(pickle.dumps(game.players[player_num]))
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            game.players[player_num] = data

            if game.players[player_num].turn:
                game.players[player_num].turn = False
                game.players[abs(game.player_num - 1)].turn = True
                game.current_player_num = game.players[abs(game.player_num - 1)]

            if player_num == 1:
                game.ready = True

            if not data:
                break
            conn.sendall(pickle.dumps(game))
        except:
            break
    game.players[player_num].connected = False
    print(addr, 'Disconnected From The Server')
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
