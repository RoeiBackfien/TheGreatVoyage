import socket
import threading
import pickle
from Game import Game

IP = '192.168.1.10'
PORT = 5555
ADDR = (IP, PORT)
currentPlayer = 0


def handle_client(conn, addr, playerNum, game):
    conn.send('Client Is Connected'.encode())
    while True:
        try:
            data = conn.recv(2048).decode()

            if playerNum == 1:
                game.ready = True

            if not data:
                print('Disconnected')
                break
            else:
                print('Received:', data)
                print('Sending:', data)

            conn.sendall(str(game.ready).encode())
        except:
            break
    print(addr, 'Lost Connection')
    conn.close()


def main():
    global currentPlayer
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ADDR)
    s.listen(2)
    print('Waiting For A Connection, Server Started')
    while True:
        if currentPlayer % 2 == 0:
            g = Game()
        conn, addr = s.accept()
        print('Connected to', addr)
        threading.Thread(target=handle_client, args=(conn, addr, currentPlayer, g)).start()
        currentPlayer += 1


if __name__ == '__main__':
    main()
