from PyQt5.QtWidgets import QApplication, QLineEdit, QPushButton, QTextBrowser, QMainWindow

class ClientUI(QMainWindow): 
    def __init__(self, app: QApplication):
        super().__init__()
        screen = app.primaryScreen()
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
        self.send_button.setGeometry(width*0.275, height*0.175, 60, 30)

        self.show()
