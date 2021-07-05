from abc import abstractmethod
import socket

from PyQt5.QtWidgets import *
import constants
import sys
from threading import Thread


class Client: #(ClientUI)

    def __init__(self):
        #super().__init__(app=QtWidgets.QApplication(sys.argv))
        #self.username = input("Username: ")
        #self.socket.connect((constants.IP, constants.PORT))
        print("in method")
        self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Thread(target=self.receive).start()
        #Thread(target=self.send).start()

    def connect(self, nickname: QLineEdit, ip_address: QLineEdit, port: QLineEdit, tabs: QTabWidget):
        port_text = port.text()
        if len(port_text) == 0 or not port_text.isnumeric():
            print("Port input must be a number and greater than 0")
            return
        try:
            self.socket_connection.connect((ip_address.text(), int(port_text)))
        except:
            print("can't connect to server...")
            self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket_connection.send(bytes("[JOINED]="+nickname.text(), constants.ENCODING))
        tabs.setTabEnabled(1, True)

        Thread(target=self.update_server).start()

    def send_message(self, message: QLineEdit):
        message_text = message.text()
        if len(message) == 0:
            return
        

    def update_server(self):
        print("in here")
        while True:
            try:
                received = self.socket_connection.recv(constants.BUFFER_SIZE).decode(constants.ENCODING)
                if received.startswith("[CLIENTS]="):
                    print(received.split("=")[1])
                else:
                    print(received)
            except socket.error as e:
                print(e)
                self.socket_connection.close()
                break

    

    def send(self) -> None:
        """
        Send input message to server
        :return: None
        """
        while True:
            self.socket.send(("[SENDTO:ALL]" + input()).encode(constants.ENCODING))

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
                    #self.messages.append(received)
            except socket.error as e:
                sys.stderr.write(e)
                self.socket.close()
                break


'''if __name__ == "__main__":
    #client = Client()

    app = QtWidgets.QApplication(sys.argv)
    client_ui = ClientUI(app)
    #client = Client(ui_client=client_ui)
    sys.exit(app.exec_())'''
