from socket import socket


class User(object):
    def __init__(self, client: socket, username: str):
        self.client = client
        self.username = username
