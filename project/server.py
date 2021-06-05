import socket
import threading

import constants
from threading import Thread


class Server(Thread):
    def __init__(self):
        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind((constants.IP, constants.PORT))
        except socket.error as e:
            print(e)
        self.socket.listen(5)

    def send(self, conn):
        while True:
            data = conn.recv(constants.BUFFER_SIZE)
            if not data: break
            print("received data:", data)
            conn.send(data)

    def run(self):
        while True:
            conn, addr = self.socket.accept()
            threading.Thread(self.send(conn))
            print("Connection address: ", addr)


if __name__ == "__main__":
    server = Server()
    server.run()
