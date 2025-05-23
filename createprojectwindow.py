from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton, QScrollArea, QWidget, QHBoxLayout
from PySide6.QtCore import Qt, QSize
import sqlite_funcs
from memberwidget import MemberWidget


class CreateProjectWindow(QDialog):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

        self.min_X = 600
        self.min_Y = 300
        self.setMinimumSize(QSize(self.min_X, self.min_Y))
        self.resize(800, 400)
        self.setWindowTitle("Create Project")


        self.layout_main = QVBoxLayout(self)

        self.label_create_project = QLabel(self)
        self.label_create_project.setText("Create Project")
        self.layout_main.addWidget(self.label_create_project)

        self.label_name_project = QLabel(self)
        self.label_name_project.setText(" Project Name:")
        self.layout_main.addWidget(self.label_name_project)

        self.input_project_name = QLineEdit(self)
        self.input_project_name.setPlaceholderText("project name")
        self.layout_main.addWidget(self.input_project_name)

        self.label_add_members = QLabel(self)
        self.label_add_members.setText(" Add Members:")
        self.layout_main.addWidget(self.label_add_members)

        self.input_member_username = QLineEdit(self)
        self.input_member_username.setPlaceholderText("member username")
        self.input_member_username.setText("1000")
        validator = QIntValidator()
        validator.setRange(1000, 9999)
        self.input_member_username.setValidator(validator)
        self.layout_main.addWidget(self.input_member_username)

        self.button_add_member = QPushButton("Add Member")
        self.button_add_member.setMaximumWidth(150)
        self.button_add_member.clicked.connect(self.add_member)
        self.layout_main.addWidget(self.button_add_member)

        self.label_error_add_member = QLabel(self)
        self.label_error_add_member.setStyleSheet("color: red")
        self.layout_main.addWidget(self.label_error_add_member)

        self.scroll_area_members = QScrollArea(self)
        self.scroll_area_members.setWidgetResizable(True)
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

        self.button_create = QPushButton("Create Project")
        self.button_create.setMaximumWidth(150)
        self.button_create.clicked.connect(self.create_project)
        self.layout_buttons.addWidget(self.button_create)

        self.button_cancel = QPushButton("Cancel")
        self.button_cancel.setMaximumWidth(150)
        self.button_cancel.clicked.connect(self.close)
        self.layout_buttons.addWidget(self.button_cancel)

    def add_member(self):
        username = int(self.input_member_username.text())
        if sqlite_funcs.username_exists(username):
            user_data = sqlite_funcs.get_user_data(username)
            member_widget = MemberWidget(username, user_data["first name"], user_data["last name"])
            self.layout_members.insertWidget(self.layout_members.count()-1,member_widget)

    def create_project(self):
        name = self.input_project_name.text()
        usernames = self.get_usernames()
        self.main_window.project_id = sqlite_funcs.project_register(name, usernames, sqlite_funcs.get_userid_with_username(self.main_window.username))
        self.close()

    def get_usernames(self):
        usernames = []
        layout = self.layout_members
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()

            if widget and isinstance(widget, MemberWidget):
                usernames.append(widget.username)
        return list(dict.fromkeys(usernames)) #remove duplicates

