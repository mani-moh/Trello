from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__ (self):
        super().__init__()
        self.setMinimumSize(QSize(400,300))
        self.setWindowTitle("my App")

        self.button = QPushButton("switch on")
        self.button.setMaximumSize(QSize(self.width()//4, self.height()//10))
        self.button.setCheckable(True)
        self.button.clicked.connect(self.button_clicked)

        #Set up the button as our central widget
        self.setCentralWidget(self.button)

    def button_clicked(self, state):
        self.button.setText("switch off" if state else "switch on")
        print(f"button is {"on" if state else "off"}")

