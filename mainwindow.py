from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__ (self):
        super().__init__()
        self.setMinimumSize(QSize(400,300))
        self.setWindowTitle("my App")
        button = QPushButton("Press Me!")

        #Set up the button as our central widget
        self.setCentralWidget(button)

