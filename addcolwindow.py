from PySide6.QtGui import QIntValidator, QCloseEvent
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QScrollArea, QWidget, QHBoxLayout, \
    QDateTimeEdit, QComboBox
from PySide6.QtCore import Qt, QSize, QDateTime
import sqlite_funcs
from memberwidget import MemberWidget
from datetime import datetime


class AddColWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window


        self.min_X = 600
        self.min_Y = 300
        self.setMinimumSize(QSize(self.min_X, self.min_Y))
        self.resize(800, 400)
        self.setWindowTitle("Add Card")

        self.layout = QVBoxLayout(self)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll)

        self.main_widget = QWidget()
        self.scroll.setWidget(self.main_widget)
        self.layout_main = QVBoxLayout(self.main_widget)






        self.input_name = QLineEdit(self)
        self.input_name.setPlaceholderText("name")
        self.input_name.setMaximumWidth(200)
        self.layout_main.addWidget(self.input_name)




        self.layout_main.addStretch()





        self.widget_buttons = QWidget()
        self.layout_main.addWidget(self.widget_buttons)

        self.layout_buttons = QHBoxLayout(self.widget_buttons)

        self.button_create = QPushButton("Create SubBoard")
        self.button_create.setMaximumWidth(150)
        self.button_create.clicked.connect(self.create_col)
        self.layout_buttons.addWidget(self.button_create)

        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.setMaximumWidth(150)
        self.button_cancel.clicked.connect(self.close)
        self.layout_buttons.addWidget(self.button_cancel)






    def closeEvent(self, event: QCloseEvent):
        self.main_window.update_trello()
        super().closeEvent(event)

    def create_col(self):

        name = self.input_name.text()
        project_id = self.main_window.project_id
        sqlite_funcs.create_subboard(name, project_id)
        self.close()