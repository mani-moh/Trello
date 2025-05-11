from PySide6.QtCore import QSize
from PySide6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget

class MainWindow(QMainWindow):
    def __init__ (self):
        super().__init__()
        self.setMinimumSize(QSize(400,300))
        self.setWindowTitle("my App")

        # self.button = QPushButton("press")
        # self.button.setMaximumSize(QSize(self.width()//4, self.height()//10))
        # #self.button.setCheckable(True)
        # self.button.clicked.connect(self.button_clicked)
        #
        # #Set up the button as our central widget
        # self.setCentralWidget(self.button)
        self.label = QLabel(self)
        self.input_text = QLineEdit(self)
        self.input_text.textChanged.connect(lambda x :self.label.setText(x.upper()))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.input_text)
        self.layout.addWidget(self.label)

        self.container = QWidget(self)
        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)

