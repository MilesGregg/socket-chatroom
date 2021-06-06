import socket
import constants
from threading import Thread


class Client:
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self):
        while True:
            self.socket.send(input().encode())

    def __init__(self):
        self.socket.connect((constants.IP, constants.PORT))
        thread = Thread(target=self.send_message())
        thread.daemon = True
        thread.start()
        while True:
            server_data = self.socket.recv(constants.BUFFER_SIZE)
            if not server_data:
                break
            print(str(server_data))


if __name__ == "__main__":
    client = Client()
