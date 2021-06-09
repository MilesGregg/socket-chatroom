import socket
import sys

import constants
from threading import Thread
from user import User


class Server:
    connections = []
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self) -> None:
        self.socket.bind((constants.IP, constants.PORT))
        self.socket.listen()

        while True:
            client, address = self.socket.accept()
            client.send('Username'.encode(constants.ENCODING))
            username = client.recv(constants.BUFFER_SIZE).decode(constants.ENCODING)
            print(username + " connected at: ", str(address))
            self.connections.append(User(client, username))
            self.send_to_clients(username.encode(constants.ENCODING) + " entered the chat room".encode(constants.ENCODING))
            Thread(target=self.receive_information, args=(client, username)).start()

    def receive_information(self, client: socket, username: str) -> None:
        """
        receives current incoming information from the client
        :param client: current client socket
        :param username: current users username
        :return: None
        """
        while True:
            try:
                message = client.recv(constants.BUFFER_SIZE)
                self.send_to_clients(message)
            except socket.error as e:
                sys.stderr.write(e)
                self.connections.remove(client)
                client.close()
                self.send_to_clients(username.encode(constants.ENCODING) + " left the chat room".encode(constants.ENCODING))
                break

    def send_to_clients(self, message: bytes) -> None:
        """
        Send message to all clients
        :param message: Message to send
        :return: None
        """
        for connection in self.connections:
            connection.client.send(message)


if __name__ == "__main__":
    server = Server()
