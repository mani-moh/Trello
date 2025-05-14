from PySide6.QtCore import QSize
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QMainWindow, QPushButton, QLineEdit, QLabel, QVBoxLayout, QWidget
from utils import clamp

class MainWindow(QMainWindow):
    def __init__ (self):
        super().__init__()
        self.WINDOW_X = 800
        self.WINDOW_Y = 600
        self.setMinimumSize(QSize(self.WINDOW_X,self.WINDOW_Y))
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


        self.label_cords = QLabel(self)
        self.label_cords.setText(f"{0}x{0}")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.input_text)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.label_cords)

        self.container = QWidget(self)
        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)
    def mouseMoveEvent (self, e : QMouseEvent):
        size = self.size()
        self.label_cords.setText(f"{clamp(e.pos().x(), 0, size.width())}x{clamp(e.pos().y(), 0, size.height())}")