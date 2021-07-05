import socket
from threading import Thread
import sys
import constants
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

class ClientUIWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent=parent)

        #self.client_util = Client()
        self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.window_layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.home_tab = QWidget()
        self.chat_tab = QWidget()
        self.tabs.addTab(self.home_tab, "Connect")
        self.tabs.addTab(self.chat_tab, "Chat")
        self.tabs.setTabEnabled(1, True)

        self.set_home_tab(home_tab=self.home_tab)
        self.set_chat_tab(chat_tab=self.chat_tab)

        self.window_layout.addWidget(self.tabs)
        self.setLayout(self.window_layout)

    def set_home_tab(self, home_tab: QWidget):
        grid = QGridLayout()
        home_tab.setLayout(grid)

        # nickname
        self.nickname = QLabel(self)
        self.nickname.setText("Nickname:")
        self.nickname_input = QLineEdit(self)
        self.nickname_input.setStyleSheet("background-color:rgb(53, 53, 53)")
        grid.addWidget(self.nickname, 0, 0, 1, 1)
        grid.addWidget(self.nickname_input, 0, 1, 1, 1)

        # ip address
        self.ip_address = QLabel(self)
        self.ip_address.setText("IP Address:")
        self.ip_address_input = QLineEdit(self)
        self.ip_address_input.setText("127.0.0.1")
        self.ip_address_input.setStyleSheet("background-color:rgb(53, 53, 53)")
        grid.addWidget(self.ip_address, 1, 0, 1, 1)
        grid.addWidget(self.ip_address_input, 1, 1, 1, 1)

        # port
        self.port = QLabel(self)
        self.port.setText("Port:")
        self.port_input = QLineEdit(self)
        self.port_input.setText("5031")
        self.port_input.setStyleSheet("background-color:rgb(53, 53, 53)")
        grid.addWidget(self.port, 2, 0, 1, 1)
        grid.addWidget(self.port_input, 2, 1, 1, 1)

        # connect button
        self.connect = QPushButton("Connect")
        self.connect.setStyleSheet("background-color:rgb(25, 106, 255)")
        self.connect.clicked.connect(self.connect_to_server)
        self.disconnect = QPushButton("Disconnect")
        self.disconnect.setStyleSheet("background-color:rgb(25, 106, 255)")
        grid.addWidget(self.connect, 3, 0, 1, 1)
        grid.addWidget(self.disconnect, 3, 1, 1, 1)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

    def set_chat_tab(self, chat_tab: QWidget):
        grid = QGridLayout()
        chat_tab.setLayout(grid)

        # chat messages
        self.messages = QTextBrowser(self)
        self.messages.setStyleSheet("background-color:rgb(53, 53, 53)")
        for i in range(50):
            self.messages.append("testing")

        # chat users
        self.chat_users = QTextBrowser(self)
        self.chat_users.setStyleSheet("background-color:rgb(53, 53, 53)")
        for i in range(50):
            self.chat_users.append("testing")

        grid.addWidget(self.messages, 0, 0, 1, 2)
        grid.addWidget(self.chat_users, 0, 2, 2, 2)

        # send message to
        self.send_to_message = QLabel("To: ", self)
        self.send_to = QComboBox(self)
        self.send_to.addItem("Everyone")
        grid.addWidget(self.send_to_message, 1, 0, 1, 1)
        grid.addWidget(self.send_to, 1, 1, 1, 1)

        # message and send button
        self.message = QLineEdit()
        self.message.returnPressed.connect(self.send_message)
        self.message.setStyleSheet("background-color:rgb(53, 53, 53)")
        self.send_message_btn = QPushButton("Send")
        self.send_message_btn.clicked.connect(self.send_message)
        self.send_message_btn.setStyleSheet("background-color:rgb(25, 106, 255)")
        grid.addWidget(self.message, 2, 0, 1, 1)
        grid.addWidget(self.send_message_btn, 2, 1, 1, 1)

    def send_message(self):
        self.messages.append(self.message.text())

    def connect_to_server(self):
        port_text = self.port_input.text()
        if len(port_text) == 0 or not port_text.isnumeric():
            print("Port input must be a number and greater than 0")
            return
        try:
            self.socket_connection.connect((self.ip_address_input.text(), int(port_text)))
        except:
            print("can't connect to server...")
            self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.socket_connection.send(bytes("[JOINED]="+self.nickname_input.text(), constants.ENCODING))
        self.tabs.setTabEnabled(1, True)

        Thread(target=self.update_server).start()

    def disconnect_from_server(self):
        self.socket_connection.close()

    def send_message(self, message: QLineEdit):
        message_text = message.text()
        if len(message) == 0:
            return
        
        
        
    def update_server(self):
        print("in here")
        while True:
            try:
                received = self.socket_connection.recv(constants.BUFFER_SIZE).decode(constants.ENCODING)
                print("message from server = " + received)
                if received.startswith("[CLIENTS]="):
                    clients = received.split("[CLIENTS]=")[1].split("-")
                    self.send_to.clear()
                    for client in clients:
                        self.send_to.addItem(client)
                else:
                    print(received)
            except socket.error as e:
                print(e)
                self.socket_connection.close()
                break


class ClientUIWindow(QMainWindow):
    def __init__(self):
        super(ClientUIWindow, self).__init__()

        self.setWindowTitle("client")
        self.setGeometry(0, 0, 500, 300)
        self.client = ClientUIWidget(self)
        self.setCentralWidget(self.client)
        self.show()

    def closeEvent(self, event):
        self.client.disconnect_server()


def set_dark_theme():
    app.setStyle('fusion')
    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(15, 15, 15))
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Text, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(30, 144, 255).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    set_dark_theme()
    c = ClientUIWindow()
    sys.exit(app.exec_())
