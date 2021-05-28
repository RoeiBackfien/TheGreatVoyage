import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = '127.0.0.1'
        self.port = 5555
        self.addr = (self.server, self.port)
        self.game = self.connect()

    def get_game(self):
        return self.game

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(9999))
        except:
            pass

    def send_str_get_obj(self, data):
        try:
            self.client.send(data.encode())
            return pickle.loads(self.client.recv(9999))
        except socket.error as e:
            print(e)

    def send_str_get_str(self, data):
        try:
            self.client.send(data.encode())
            return self.client.recv(9999)
        except socket.error as e:
            print(e)

    def send_str(self, data):
        try:
            self.client.send(data.encode())
        except socket.error as e:
            print(e)

    def recv_str(self):
        try:
            return self.client.recv(9999).decode()
        except socket.error as e:
            print(e)

    def send_obj_recv_obj(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(9999))
        except socket.error as e:
            print(e)

    def send_obj(self, data):
        try:
            self.client.send(pickle.dumps(data))
        except socket.error as e:
            print(e)

    def recv_obj(self):
        try:
            return pickle.loads(self.client.recv(9999))
        except socket.error as e:
            print(e)
