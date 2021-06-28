import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

class ClientUIWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent=parent)

        self.window_layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.home_tab = QWidget()
        self.chat_tab = QWidget()
        self.tabs.addTab(self.home_tab, "Connect")
        self.tabs.addTab(self.chat_tab, "Chat")
        self.tabs.setTabEnabled(1, False)

        self.set_home_tab(home_tab=self.home_tab)

        self.window_layout.addWidget(self.tabs)
        self.setLayout(self.window_layout)

    def set_home_tab(self, home_tab: QWidget):
        grid = QGridLayout()
        home_tab.setLayout(grid)

        # nickname
        self.nickname = QLabel(self)
        self.nickname.setText('Nickname:')
        self.nickname_input = QLineEdit(self)
        self.nickname_input.setStyleSheet("background-color:white")
        grid.addWidget(self.nickname, 0, 0, 1, 1)
        grid.addWidget(self.nickname_input, 0, 1, 1, 1)

        # ip address
        self.ip_address = QLabel(self)
        self.ip_address.setText('IP Address:')
        self.ip_address_input = QLineEdit(self)
        self.ip_address_input.setStyleSheet("background-color:white")
        grid.addWidget(self.ip_address, 1, 0, 1, 1)
        grid.addWidget(self.ip_address_input, 1, 1, 1, 1)

        # port
        self.port = QLabel(self)
        self.port.setText('Port:')
        self.port_input = QLineEdit(self)
        self.port_input.setStyleSheet("background-color:white")
        grid.addWidget(self.port, 2, 0, 1, 1)
        grid.addWidget(self.port_input, 2, 1, 1, 1)

        # connect button
        self.connect = QPushButton("Connect")
        self.connect.setStyleSheet("background-color:rgb(25, 106, 255)")
        self.disconnect = QPushButton("Disconnect")
        self.disconnect.setStyleSheet("background-color:rgb(25, 106, 255)")
        grid.addWidget(self.connect, 3, 0, 1, 1)
        grid.addWidget(self.disconnect, 3, 1, 1, 1)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)

    def set_chat_tab(self, chat_tab: QWidget):
        grid = QGridLayout()


class ClientUI(QMainWindow):
    def __init__(self):
        super(ClientUI, self).__init__()

        self.setWindowTitle("client")
        self.setGeometry(100, 100, 400, 400)
        self.setCentralWidget(ClientUIWidget(self))
        self.show()


        '''screen = app.primaryScreen()
        width = float(screen.size().width())
        height = float(screen.size().width())
        self.setWindowTitle("client")
        self.setGeometry(width*0.2, height*0.2, width*0.35, height*0.25)
        
        self.messages = QTextBrowser(self)
        self.messages.setGeometry(30, 30, width*0.25, height*0.15)
        for i in range(100):
            self.messages.append("testing messages")

        self.input_message = QLineEdit(self)
        self.input_message.setPlaceholderText("Type message...")
        self.input_message.setGeometry(30, height*0.175, width*0.25, height*0.02)
 
        self.send_button = QPushButton("Send", self)
        self.send_button.setGeometry(width*0.275, height*0.175, 60, 30)'''


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
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(142, 45, 197).lighter())
    palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(palette)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    set_dark_theme()
    c = ClientUI()
    sys.exit(app.exec_())
