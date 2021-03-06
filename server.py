import os
import socket
import sys

import constants
import time
from threading import Thread

class Server:
    def __init__(self) -> None:
        # setup TCP communication
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((constants.IP, constants.PORT))
        self.connections = {}

        print("Started server on -> address: {address} | port: {port}".format(address=constants.IP, port=constants.PORT))

        try:
            self.socket.listen()
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

    def handle_incoming(self) -> None:
        """
        handle all incoming client connections and handle them by making new thread for each client
        """
        while True:
            client, address = self.socket.accept()
            Thread(target=self.update, args=(client,)).start()

    def update(self, client: socket) -> None:
        """
        receives current incoming information from the client
        :param client: current client socket
        :param username: current users username

        :return: None
        """
        client_nickname = ""
        while True:
            # decode the incoming message using utf-8
            message = client.recv(constants.BUFFER_SIZE).decode(constants.ENCODING)

            if message.startswith("[SENDTO:ALL]") and client_nickname:
                self.send_to_clients(bytes(message.replace("[SENDTO:ALL]", "[SENDTO:ALL:" + client_nickname + "]"), constants.ENCODING))
                continue
            elif message.startswith("[SENDTO") and client_nickname:
                message_split = message.split("]")
                name = message_split[0][1:].split(":")[1]
                for client_sock, client_name in self.connections.items():
                    if name == client_name:
                        client_sock.send(bytes("[SENDTO:" + client_nickname + "]=" + message_split[1].split("=")[1], constants.ENCODING))
                continue
            elif message.startswith("[JOINED]"):
                client_nickname = message.split("=")[1]
                current_clients = []
                [current_clients.append(client_name) for _, client_name in self.connections.items()]
                if client_nickname in current_clients:
                    client.send(bytes("[DUPLICATE]" + client_nickname, constants.ENCODING))
                    continue
                time.sleep(0.1)
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
