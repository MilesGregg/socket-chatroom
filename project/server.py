import socket

import constants
from threading import Thread

class User(object):
    def __init__(self, client: socket, username: str):
        self.client = client
        self.username = username

class Server:
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self) -> None:
        self.socket.bind((constants.IP, constants.PORT))
        self.socket.listen()
        self.connections = []

        try:
            while True:
                client, address = self.socket.accept()
                '''client.send('Username'.encode(constants.ENCODING))
                username = client.recv(constants.BUFFER_SIZE).decode(constants.ENCODING)
                print(username + " connected at: ", str(address))
                self.connections.append(User(client, username))
                self.send_to_clients(username.encode(constants.ENCODING) + " entered the chat room".encode(constants.ENCODING))'''
                Thread(target=self.receive_information, args=(client,)).start()
        except KeyboardInterrupt:
            self.socket.close()

    def receive_information(self, client: socket) -> None:
        """
        receives current incoming information from the client
        :param client: current client socket
        :param username: current users username
        :return: None
        """
        while True:
            try:
                message = client.recv(constants.BUFFER_SIZE).decode(constants.ENCODING)

                print("message received: " + message)

                if message.startswith("[SENDTO:ALL]"):
                    #message.split
                    print("receiveved message")
                    #self.send_to_clients(message.split("]"))

                if message.startswith("[JOINED]"):
                    self.connections.append(User(client, message.split("=")[1]))
                    print("someone joined")
                    self.send_to_clients(bytes(message.split("=")[1] + " joined the chat!", constants.ENCODING))
                    clients = []
                    for connection in self.connections:
                        clients.append(connection.username)
                        #print(connection.username)
                    self.send_to_clients(bytes("[CLIENTS]=" + "-".join(clients), constants.ENCODING))

                elif message.startswith("[LEFT]"):
                    client.close()
                    self.connections.remove(client)
                    break
                    

                #self.send_to_clients(message)
            except socket.error as e:
                self.connections.remove(client)
                client.close()
                #self.send_to_clients(username.encode(constants.ENCODING) + " left the chat room".encode(constants.ENCODING))
                break

    def append_usernames(self):
        users = []
        for i in self.connections:
            print(i)
        return -1

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
