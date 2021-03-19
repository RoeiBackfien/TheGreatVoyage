import socket
import threading
import pickle
from Game import Game

IP = '192.168.1.10'
PORT = 5555
ADDR = (IP, PORT)


def handle_client(conn, addr, player_num, game):
    conn.send(f'You Are Player Number {player_num}'.encode())
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            game.players[player_num] = data

            if player_num == 1:
                game.ready = True

            if not data:
                break

            conn.sendall(pickle.dumps(game))
        except:
            break
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
        threading.Thread(target=handle_client, args=(conn, addr, currentPlayer, game)).start()
        currentPlayer += 1


if __name__ == '__main__':
    main()
