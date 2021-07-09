import re
import socket
import os
from threading import Thread
import sys
import time
import constants
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

class ClientUIWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent=parent)

        # sockect communication and connection
        self.connected = False
        self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # main window and tabs layout for gui
        self.window_layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.home_tab = QWidget()
        self.chat_tab = QWidget()
        self.tabs.addTab(self.home_tab, "Connect")
        self.tabs.addTab(self.chat_tab, "Chat")
        self.tabs.setTabEnabled(1, False)

        self.set_home_tab(home_tab=self.home_tab)
        self.set_chat_tab(chat_tab=self.chat_tab)

        self.window_layout.addWidget(self.tabs)
        self.setLayout(self.window_layout)

    def set_home_tab(self, home_tab: QWidget) -> None:
        """
        setup the home tab gui
        :param home_tab: home tab Qidget to modify that specific tab
        
        :return: None
        """
        grid = QGridLayout()
        home_tab.setLayout(grid)

        # nickname
        self.nickname = QLabel(self)
        self.nickname.setText("Nickname:")
        self.nickname_input = QLineEdit(self)
        self.nickname_input.setStyleSheet(constants.INPUT_COLOR)
        grid.addWidget(self.nickname, 0, 0, 1, 1)
        grid.addWidget(self.nickname_input, 0, 1, 1, 1)

        # ip address
        self.ip_address = QLabel(self)
        self.ip_address.setText("IP Address:")
        self.ip_address_input = QLineEdit(self)
        self.ip_address_input.setText("127.0.0.1")
        self.ip_address_input.setStyleSheet(constants.INPUT_COLOR)
        grid.addWidget(self.ip_address, 1, 0, 1, 1)
        grid.addWidget(self.ip_address_input, 1, 1, 1, 1)

        # port
        self.port = QLabel(self)
        self.port.setText("Port:")
        self.port_input = QLineEdit(self)
        self.port_input.setText("2532")
        self.port_input.setStyleSheet(constants.INPUT_COLOR)
        grid.addWidget(self.port, 2, 0, 1, 1)
        grid.addWidget(self.port_input, 2, 1, 1, 1)

        # connect button
        self.connect = QPushButton("Connect")
        self.connect.setStyleSheet(constants.BUTTON_COLOR)
        self.connect.clicked.connect(self.connect_to_server)
        self.disconnect = QPushButton("Disconnect")
        self.disconnect.setStyleSheet(constants.BUTTON_COLOR)
        self.disconnect.clicked.connect(lambda: self.disconnect_from_server(False))
        grid.addWidget(self.connect, 3, 0, 1, 1)
        grid.addWidget(self.disconnect, 3, 1, 1, 1)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

    def set_chat_tab(self, chat_tab: QWidget):
        """
        setup the chat tab gui
        :param chat_tab: home tab Qidget to modify that specific tab

        :return: None
        """
        grid = QGridLayout()
        chat_tab.setLayout(grid)

        # chat messages
        self.messages = QListView()
        self.messages.setWindowTitle("Messages")
        self.messages.setStyleSheet(constants.INPUT_COLOR)
        self.messages_model = QtGui.QStandardItemModel(self.messages)
        self.messages.setModel(self.messages_model)

        # chat users
        self.chat_users = QListView()
        self.chat_users.setWindowTitle("Chat Users")
        self.chat_users.setStyleSheet(constants.INPUT_COLOR)
        self.chat_model = QtGui.QStandardItemModel(self.chat_users)
        self.chat_users.setModel(self.chat_model)
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
        self.message.setStyleSheet(constants.INPUT_COLOR)
        self.send_message_btn = QPushButton("Send")
        self.send_message_btn.clicked.connect(self.send_message)
        self.send_message_btn.setStyleSheet(constants.BUTTON_COLOR)
        grid.addWidget(self.message, 2, 0, 1, 1)
        grid.addWidget(self.send_message_btn, 2, 1, 1, 1)

    def connect_to_server(self) -> None:
        """
        Attempt to connect to the specified server depending on the 3 different inputs, if the server is not open
        then the client will not connect to the server. All of the inputs must be length > 0 to connect to the server.
        The client will create a new thread to handle all of the server messages in and out.

        :return: None
        """
        port_text = self.port_input.text()
        ip_address_text = self.ip_address_input.text()
        self.connected_username = self.nickname_input.text()
        if bool(re.match("^[0-9\.]*$", ip_address_text)) == False:
            print("IP address must be numbers and periods only")
            return
        elif not port_text.isnumeric():
            print("Port must be numeric")
            return
        elif len(self.nickname_input.text()) == 0 or len(ip_address_text) == 0 or len(port_text) == 0:
            print("Nickname, IP Address, and Port input must be a number and greater than 0 characters long")
            return
        try:
            self.socket_connection.connect((ip_address_text, int(port_text)))
        except:
            print("can't connect to server...")
            self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            return
        self.connected = True
        self.socket_connection.send(bytes("[JOINED]=" + self.nickname_input.text(), constants.ENCODING))
        self.tabs.setTabEnabled(1, True)
        self.thread = Thread(target=self.update)
        self.thread.start()

    def disconnect_from_server(self, dulplicate) -> None:
        """
        Distconnect to the current server that the client is connected to and will reconnect when entering a new
        nickname, ip address, and port number.

        :return: None
        """
        if self.connected == False:
            return
        if dulplicate == False:
            self.socket_connection.send(bytes("[LEFT]="  + self.nickname_input.text(), constants.ENCODING))
        self.connected = False
        self.tabs.setTabEnabled(1, False)
        #self.thread.join()
        self.socket_connection.close()
        self.socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self) -> None:
        """
        This function will send a message that is > 0 characters in length to the server. It handles if the message need to be
        sent to all of the connected clients or a specific one.

        :return: None
        """
        message_text = self.message.text()
        if len(message_text) == 0:
            return
        if self.send_to.currentText() == "Everyone":
            self.socket_connection.send(bytes("[SENDTO:ALL]=" + message_text, constants.ENCODING))
        else:
            self.socket_connection.send(bytes("[SENDTO:" + self.connected_username + "]=" + message_text, constants.ENCODING))
            time.sleep(0.1)
            self.socket_connection.send(bytes("[SENDTO:" + self.send_to.currentText() + "]=" + message_text, constants.ENCODING))
        self.message.clear()
        
    def update(self) -> None:
        """
        Handles all of the messages sent from the server to the clients and then chooses what to do with the message. If the message
        is about clients then it will update the chat users list. If the message needs to be displayed it will display the message
        on the main text feed. Then finally it will handle any disconnections from the server.

        :return: None
        """
        while self.connected: 
            received = self.socket_connection.recv(constants.BUFFER_SIZE).decode(constants.ENCODING)
            if not received:
                print("disconnected from server!")
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)

            if received.startswith("[DUPLICATE]"):
                print("Duplicate username found!")
                self.disconnect_from_server(True)
            elif received.startswith("[CLIENTS]="):
                clients = received.split("[CLIENTS]=")[1].split("-")
                self.chat_model.clear()
                top_item = QtGui.QStandardItem("All Users:\n")
                top_item.setCheckable(False)
                self.chat_model.appendRow(top_item)
                self.send_to.clear()
                self.send_to.addItem("Everyone")
                for client in clients:
                    item = QtGui.QStandardItem(client)
                    item.setCheckable(False)
                    self.chat_model.appendRow(item)
                    if client != self.connected_username:
                        self.send_to.addItem(client)
            elif received.startswith("[SENDTO:ALL:"):
                name = received.split("]")[0][1:].split(":")[2] + ": "
                item = QtGui.QStandardItem(name + received.split("=")[1])
                item.setCheckable(False)
                self.messages_model.appendRow(item)
            elif received.startswith("[SENDTO:"):
                name = received.split("]")[0][1:].split(":")[1] + ": "
                item = QtGui.QStandardItem(name + received.split("=")[1])
                item.setCheckable(False)
                self.messages_model.appendRow(item)
            elif received.startswith("[JOINED]="):
                item = QtGui.QStandardItem(received.split("=")[1] + " joined the chat!")
                item.setCheckable(False)
                self.messages_model.appendRow(item)
            elif received.startswith("[LEFT]="):
                item = QtGui.QStandardItem(received.split("=")[1] + " left the chat!")
                item.setCheckable(False)
                self.messages_model.appendRow(item)
            time.sleep(0.1)


class ClientUIWindow(QMainWindow):
    def __init__(self):
        super(ClientUIWindow, self).__init__()

        self.setWindowTitle("client")
        self.setGeometry(0, 0, 500, 300)
        self.client = ClientUIWidget(self)
        self.setCentralWidget(self.client)
        self.show()

    def closeEvent(self, event) -> None:
        """
        When closing out of the main window disonnect from the server.

        :return: None
        """
        self.client.disconnect_from_server(False)

def set_dark_theme() -> None:
    """
    Set dark theme to the window.

    :return: None
    """
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
