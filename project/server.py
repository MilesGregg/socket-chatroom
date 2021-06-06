import socket
import constants
from threading import Thread


class Server:
    connections = []
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        try:
            self.socket.bind((constants.IP, constants.PORT))
        except socket.error as e:
            print(e)
        self.socket.listen(100)

    def send(self, connection):
        while True:
            received_data = connection.recv(constants.BUFFER_SIZE)
            for c in self.connections:
                c.send(received_data)
            if not received_data:
                self.connections.remove(connection)
                connection.close()
                break

    def run(self):
        while True:
            conn, addr = self.socket.accept()
            thread = Thread(self.send(conn))
            thread.daemon = True
            thread.start()
            self.connections.append(conn)
            print("New Connection: ", addr)


if __name__ == "__main__":
    server = Server()
    server.run()
