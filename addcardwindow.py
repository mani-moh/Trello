from PySide6.QtGui import QIntValidator, QCloseEvent
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QScrollArea, QWidget, QHBoxLayout, \
    QDateTimeEdit, QComboBox
from PySide6.QtCore import Qt, QSize, QDateTime
import sqlite_funcs
from memberwidget import MemberWidget
from datetime import datetime


class AddCardWindow(QDialog):
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



        self.input_subboard = QComboBox(self)
        s_name = self.main_window.subboard_name
        for sid in s_name:
            self.input_subboard.addItem(f"{s_name[sid]}", sid)
        self.layout_main.addWidget(self.input_subboard)


        self.input_name = QLineEdit(self)
        self.input_name.setPlaceholderText("name")
        self.input_name.setMaximumWidth(200)
        self.layout_main.addWidget(self.input_name)


        self.input_description = QLineEdit(self)
        self.input_description.setPlaceholderText("description")
        self.input_description.setMaximumWidth(600)
        self.layout_main.addWidget(self.input_description)

        label_deadline = QLabel(self)
        label_deadline.setText("Deadline:")
        self.layout_main.addWidget(label_deadline)
        self.input_deadline = QDateTimeEdit(self)
        self.input_deadline.setDateTime(QDateTime.currentDateTime())
        self.input_deadline.setCalendarPopup(True)
        self.layout_main.addWidget(self.input_deadline)

        label_priority = QLabel(self)
        label_priority.setText("Priority:")
        self.layout_main.addWidget(label_priority)
        self.input_priority = QComboBox(self)
        for i in range(1,6):
            self.input_priority.addItem(f"{i}", i)
        self.layout_main.addWidget(self.input_priority)


        self.label_add_members = QLabel(self)
        self.label_add_members.setText("\nAdd Members:")
        self.layout_main.addWidget(self.label_add_members)

        self.input_members = QLineEdit(self)
        self.input_members.setPlaceholderText("member username")
        self.input_members.setMaximumWidth(600)
        validator = QIntValidator()
        validator.setRange(1000, 9999)
        self.input_members.setValidator(validator)
        self.layout_main.addWidget(self.input_members)
        self.button_members = QPushButton(self)
        self.button_members.setText("Add member")
        self.button_members.clicked.connect(self.add_member)
        self.button_members.setMaximumWidth(200)
        self.layout_main.addWidget(self.button_members)



        self.label_error_add_member = QLabel(self)
        self.label_error_add_member.setStyleSheet("color: red")
        self.layout_main.addWidget(self.label_error_add_member)

        self.scroll_area_members = QScrollArea(self)
        self.scroll_area_members.setWidgetResizable(True)
        self.scroll_area_members.setMinimumHeight(200)
        self.scroll_area_members.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scroll_area_members.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.layout_main.addWidget(self.scroll_area_members)

        self.layout_main.addStretch()

        self.widget_members = QWidget()
        self.scroll_area_members.setWidget(self.widget_members)

        self.layout_members = QVBoxLayout(self.widget_members)
        self.layout_members.addStretch()



        self.widget_buttons = QWidget()
        self.layout_main.addWidget(self.widget_buttons)

        self.layout_buttons = QHBoxLayout(self.widget_buttons)

        self.button_create = QPushButton("Create Card")
        self.button_create.setMaximumWidth(150)
        self.button_create.clicked.connect(self.create_card)
        self.layout_buttons.addWidget(self.button_create)

        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.setMaximumWidth(150)
        self.button_cancel.clicked.connect(self.close)
        self.layout_buttons.addWidget(self.button_cancel)


    def add_member(self):
        username = int(self.input_members.text())
        if sqlite_funcs.username_exists(username):
            user_data = sqlite_funcs.get_user_data(username)
            member_widget = MemberWidget(username, user_data["first name"], user_data["last name"])
            self.layout_members.insertWidget(self.layout_members.count()-1,member_widget)




    def get_usernames(self):
        usernames = []
        layout = self.layout_members
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()

            if widget and isinstance(widget, MemberWidget):
                usernames.append(widget.username)
        return list(dict.fromkeys(usernames)) #remove duplicates



    def closeEvent(self, event: QCloseEvent):
        self.main_window.update_trello()
        super().closeEvent(event)

    def create_card(self):
        sid = self.input_subboard.currentData()
        name = self.input_name.text()
        description = self.input_description.text()
        deadline = self.input_deadline.dateTime().toMSecsSinceEpoch()
        priority = self.input_priority.currentData()
        usernames = self.get_usernames()
        sqlite_funcs.create_card(sid, name, description, deadline, priority, usernames)
        self.close()