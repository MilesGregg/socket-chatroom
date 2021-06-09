import socket
import constants
import sys
from threading import Thread


class Client:
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        self.username = input("Username: ")
        self.socket.connect((constants.IP, constants.PORT))

        Thread(target=self.receive).start()
        Thread(target=self.send).start()

    def send(self) -> None:
        """
        Send input message to server
        :return: None
        """
        while True:
            self.socket.send((self.username + ": " + input()).encode(constants.ENCODING))

    def receive(self) -> None:
        """
        Gets message from the server
        :return: None
        """
        while True:
            try:
                received = self.socket.recv(constants.BUFFER_SIZE).decode(constants.ENCODING)
                if received == 'Username':
                    self.socket.send(self.username.encode(constants.ENCODING))
                else:
                    print(received)
            except socket.error as e:
                sys.stderr.write(e)
                self.socket.close()
                break


if __name__ == "__main__":
    client = Client()
