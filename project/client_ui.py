from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QWidget, QPushButton, QLabel, QMenuBar, QStatusBar, QLineEdit

class ClientUI(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setWindowTitle("client")
        self.setGeometry(10, 10, 500, 200)
    
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 40)
        
        self.show()
