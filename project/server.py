import os
import socket
import sys

import constants
import time
from threading import Thread

class Server:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((constants.IP, constants.PORT))
        self.connections = {}

        try:
            self.socket.listen(5)
            print("Server started listing...")
            main_thread = Thread(target=self.handle_incoming)
            main_thread.start()
            main_thread.join()
            self.socket.close()
        except KeyboardInterrupt:
            print("Closing server!")
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

    def handle_incoming(self):
        '''
        handle all incoming client connections and handle them by making new thread for each cleint
        '''
        while True:
            client, address = self.socket.accept()
            Thread(target=self.receive_information, args=(client,)).start()

    def receive_information(self, client: socket) -> None:
        """
        receives current incoming information from the client
        :param client: current client socket
        :param username: current users username
        :return: None
        """
        client_nickname = ""
        while True:
            message = client.recv(constants.BUFFER_SIZE).decode(constants.ENCODING)

            print("message received: " + message)

            if message.startswith("[SENDTO:ALL]") and client_nickname:
                self.send_to_clients(bytes(message.replace("[SENDTO:ALL]", "[SENDTO:ALL:" + client_nickname + "]"), constants.ENCODING))
                continue
            elif message.startswith("[SENDTO") and client_nickname:
                try :
                    message_split = message.split("]")
                    name = message_split[0][1:].split(":")[1]
                    print("NAME = " + name)
                    print("ACTUAL MESSAGE = " + message_split[1].split("=")[1])
                    for connection in self.connections:
                        print("connection usernames: " + connection.username)
                        if name == connection.username:
                            print("sending to client")
                            connection.client.send(bytes("[SENDTO:" + client_nickname + "]=" + message_split[1].split("=")[1], constants.ENCODING))
                except:
                    print("error sending to directly")

            if message.startswith("[JOINED]"):
                client_nickname = message.split("=")[1]
                self.connections[client] = client_nickname
                print(client_nickname + " joined that chat!")
                self.send_to_clients(bytes("[JOINED]=" + client_nickname, constants.ENCODING))
                time.sleep(0.1)
                clients = []
                for _, client_name in self.connections.items():
                    clients.append(client_name)
                self.send_to_clients(bytes("[CLIENTS]=" + "-".join(clients), constants.ENCODING))
                continue
            elif message.startswith("[LEFT]"):
                client.close()
                try:
                    del self.connections[client]
                except KeyError:
                    pass
                if len(client_nickname) != 0:
                    print(client_nickname + " left that chat!")
                    self.send_to_clients(bytes("[LEFT]=" + client_nickname, constants.ENCODING))
                    time.sleep(0.1)
                    clients = []
                    for _, client_name in self.connections.items():
                        clients.append(client_name)
                    self.send_to_clients(bytes("[CLIENTS]=" + "-".join(clients), constants.ENCODING))
                break

    def send_to_clients(self, message: bytes) -> None:
        """
        Send message to all clients
        :param message: Message to send
        :return: None
        """
        for connection in self.connections:
            connection.send(message)


if __name__ == "__main__":
    server = Server()
