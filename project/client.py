import socket
import constants
from threading import Thread


class Client(Thread):
    def __init__(self):
        super().__init__()
        print("Connecting to server... at --- Port: ", constants.PORT, ", IP: ", constants.IP)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((constants.IP, constants.PORT))
        except socket.error as error:
            print(error)

    def run(self):
        while True:
            message = input()
            self.socket.send(message.encode())
            serverData = self.socket.recv(constants.BUFFER_SIZE)
            print("Message received: ", serverData)

        self.socket.close()


if __name__ == "__main__":
    client = Client()
    client.run()
