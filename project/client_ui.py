import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

class ClientUIWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent=parent)

        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        self.tabs.resize(300,200)        
        self.home_tab = QWidget()
        self.tab2 = QWidget()
        self.tabs.addTab(self.tab1, "Connect")
        self.tabs.addTab(self.tab2, "Chat")
        self.tabs.setTabEnabled(1,False)
        
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)  


class ClientUI(QMainWindow): 
    def __init__(self):
        super(ClientUI, self).__init__()

        self.setWindowTitle("client")
        self.setGeometry(100, 100, 500, 500)
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
    c = ClientUI()
    sys.exit(app.exec_())
