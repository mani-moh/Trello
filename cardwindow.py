from PySide6.QtGui import QIntValidator, QCloseEvent
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QScrollArea, QWidget, QHBoxLayout, \
    QDateTimeEdit, QComboBox
from PySide6.QtCore import Qt, QSize, QDateTime
import sqlite_funcs
from memberwidget import MemberWidget
from datetime import datetime


class CardWindow(QDialog):
    def __init__(self, main_window, card_id):
        super().__init__()
        self.main_window = main_window
        self.card_id = card_id
        self.has_access = sqlite_funcs.has_access(self.main_window.username, self.card_id)
        self.data = sqlite_funcs.get_card_data(card_id)

        self.min_X = 600
        self.min_Y = 300
        self.setMinimumSize(QSize(self.min_X, self.min_Y))
        self.resize(800, 400)
        self.setWindowTitle("Card Inspect")

        self.layout = QVBoxLayout(self)
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll)

        self.main_widget = QWidget()
        self.scroll.setWidget(self.main_widget)
        self.layout_main = QVBoxLayout(self.main_widget)

        self.label_name = QLabel(self)
        self.label_name.setText(f"name: {self.data["name"]}")
        self.layout_main.addWidget(self.label_name)

        self.label_desc = QLabel(self)
        self.label_desc.setText(f"description: {self.data["description"]}")
        self.layout_main.addWidget(self.label_desc)

        self.label_card_id = QLabel(self)
        self.label_card_id.setText(f"card_id: {self.data["card_id"]}")
        self.layout_main.addWidget(self.label_card_id)

        self.label_deadline = QLabel(self)
        self.label_deadline.setText(f"deadline: {QDateTime.fromMSecsSinceEpoch(self.data["deadline"]).toString()}")
        self.layout_main.addWidget(self.label_deadline)


        self.label_priority = QLabel(self)
        self.label_priority.setText(f"priority: {self.data["priority"]}")
        self.layout_main.addWidget(self.label_priority)

        self.label_created_at = QLabel(self)
        self.label_created_at.setText(f"created_at: {self.data["created_at"]}")
        self.layout_main.addWidget(self.label_created_at)

        self.label_members = QLabel(self)
        self.label_members.setText(f"members: {self.data["members"]}")
        self.layout_main.addWidget(self.label_members)

        self.input_subboard = QComboBox(self)
        s_name = self.main_window.subboard_name
        for sid in s_name:
            self.input_subboard.addItem(f"{s_name[sid]}", sid)
        self.layout_main.addWidget(self.input_subboard)
        self.button_subboard = QPushButton(self)
        self.button_subboard.setText("Change subboard")
        self.button_subboard.clicked.connect(self.change_subboard)
        self.button_subboard.setMaximumWidth(200)
        self.layout_main.addWidget(self.button_subboard)

        self.input_name = QLineEdit(self)
        self.input_name.setText(self.data["name"])
        self.input_name.setMaximumWidth(200)
        self.layout_main.addWidget(self.input_name)
        self.button_name = QPushButton(self)
        self.button_name.setText("Change Name")
        self.button_name.clicked.connect(self.change_name)
        self.button_name.setMaximumWidth(200)
        self.layout_main.addWidget(self.button_name)

        self.input_description = QLineEdit(self)
        self.input_description.setText(self.data["description"])
        self.input_description.setMaximumWidth(600)
        self.layout_main.addWidget(self.input_description)
        self.button_description = QPushButton(self)
        self.button_description.setText("Change Description")
        self.button_description.clicked.connect(self.change_description)
        self.button_description.setMaximumWidth(200)
        self.layout_main.addWidget(self.button_description)

        self.input_deadline = QDateTimeEdit(self)
        self.input_deadline.setDateTime(QDateTime.fromMSecsSinceEpoch(self.data["deadline"]))
        self.input_deadline.setCalendarPopup(True)
        self.layout_main.addWidget(self.input_deadline)
        self.button_deadline = QPushButton(self)
        self.button_deadline.setText("Change Deadline")
        self.button_deadline.clicked.connect(self.change_deadline)
        self.button_deadline.setMaximumWidth(200)
        self.layout_main.addWidget(self.button_deadline)

        self.input_priority = QComboBox(self)
        for i in range(1,6):
            self.input_priority.addItem(f"{i}", i)
        self.layout_main.addWidget(self.input_priority)
        self.button_priority = QPushButton(self)
        self.button_priority.setText("Change Priority")
        self.button_priority.clicked.connect(self.change_priority)
        self.button_priority.setMaximumWidth(200)
        self.layout_main.addWidget(self.button_priority)

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

        self.button_save_members = QPushButton("Save members")
        self.button_save_members.setMaximumWidth(150)
        self.button_save_members.clicked.connect(self.save_members)
        self.layout_main.addWidget(self.button_save_members)

        self.widget_buttons = QWidget()
        self.layout_main.addWidget(self.widget_buttons)

        self.layout_buttons = QHBoxLayout(self.widget_buttons)



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

    def save_members(self):
        if self.has_access:
            usernames = self.get_usernames()
            sqlite_funcs.add_task_members(self.card_id, usernames)


    def get_usernames(self):
        usernames = []
        layout = self.layout_members
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()

            if widget and isinstance(widget, MemberWidget):
                usernames.append(widget.username)
        return list(dict.fromkeys(usernames)) #remove duplicates

    def change_name(self):
        if self.has_access:
            new_name = self.input_name.text()
            sqlite_funcs.change_name(self.card_id, new_name)

    def change_description(self):
        if self.has_access:
            new_description = self.input_description.text()
            sqlite_funcs.change_description(self.card_id, new_description)

    def change_deadline(self):
        if self.has_access:
            deadline = self.input_deadline.dateTime().toMSecsSinceEpoch()
            sqlite_funcs.change_deadline(self.card_id, deadline)

    def change_priority(self):
        if self.has_access:
            priority = self.input_priority.currentData()
            sqlite_funcs.change_priority(self.card_id, priority)

    def closeEvent(self, event: QCloseEvent):
        self.main_window.update_trello()
        super().closeEvent(event)

    def change_subboard(self):
        if self.has_access:
            sid = self.input_subboard.currentData()
            sqlite_funcs.change_subboard(self.card_id, sid)


