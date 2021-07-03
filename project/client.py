import socket

from PyQt5 import QtWidgets
import constants
import sys
from threading import Thread


class Client: #(ClientUI)
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __init__(self):
        #super().__init__(app=QtWidgets.QApplication(sys.argv))
        #self.username = input("Username: ")
        #self.socket.connect((constants.IP, constants.PORT))
        print()
        #Thread(target=self.receive).start()
        #Thread(target=self.send).start()

    @staticmethod
    def connect(nickname: QtWidgets.QLineEdit, ip_address: QtWidgets.QLineEdit, port: QtWidgets.QLineEdit):
        port_text = port.text()
        if len(port_text) == 0 or not port_text.isnumeric():
            print("Port input must be a number and greater than 0")
            return
        '''try:
            self.socket.connect((ip_address.text(), int(port_text)))
        except:
            print("can't connect to server.....")'''

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
