
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QScrollArea, \
    QHBoxLayout, QStackedWidget, QLineEdit

from addcardwindow import AddCardWindow
from cardwidget import CardWidget
from cardwindow import CardWindow
from colwidget import ColWidget
import sqlite_funcs
from projectwidget import ProjectWidget
from usersettingswindow import UserSettingsWindow
from createprojectwindow import CreateProjectWindow
from addcolwindow import AddColWindow


class MainWindow(QMainWindow):
    cards_style = "background-color: rgb(50, 50, 50); margin: 5px; padding: 10px; border-radius: 5px; border: 1px solid white"
    col_style = "background-color: rgb(30, 30, 30); margin: 5px; padding: 10px;"
    def __init__ (self):
        super().__init__()
        self.path = "data.json"


        self.min_X = 600
        self.min_Y = 300
        self.setMinimumSize(QSize(self.min_X,self.min_Y))
        self.resize(1000,600)
        self.setWindowTitle("Trello")
        self.scroll_cols = []
        self.num = 1
        self.username = -1
        self.project_id = 0
        self.user_data = {
            "first name": "",
            "last name": "",
            "email": "",
            "type": "",
            "is admin": False,
            "phone number": "",
            "date created": None
        }

        self.projects = {}


        #central widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.pages = {
            "login": 0,
            "projects": 1,
            "trello" : 2
        }

        self.create_login_page()
        self.create_projects_page()
        self.create_trello_page()
        self.stacked_widget.setCurrentIndex(0)
        try:
            with open("username.txt", "r") as f:
                content = f.read()
                if content.strip() != "":
                    self.username = content.strip()
                    self.update_projects_page()
                    self.update_projects()
                    self.stacked_widget.setCurrentIndex(self.pages["projects"])
        except FileNotFoundError:
            pass

    def create_trello_page(self):

        #main layout v
        self.central_widget_trello = QWidget()
        self.stacked_widget.addWidget(self.central_widget_trello)
        self.layout_main = QVBoxLayout(self.central_widget_trello)

        #label
        self.label_board_name = QLabel(self)
        self.label_board_name.setText("Board Name")
        self.layout_main.addWidget(self.label_board_name)

        #button add col
        self.button_add_column = QPushButton("Add Column")
        self.button_add_column.clicked.connect(self.slot_button_add_column)
        self.layout_main.addWidget(self.button_add_column)

        # button add card
        self.button_add_card = QPushButton("Add Card")
        self.button_add_card.clicked.connect(self.slot_button_add_card)
        self.layout_main.addWidget(self.button_add_card)

        self.button_close_project = QPushButton("Close Project")
        self.button_close_project.clicked.connect(self.close_project)
        self.layout_main.addWidget(self.button_close_project)

        #widget trello
        self.widget_trello = QWidget()
        self.layout_main.addWidget(self.widget_trello)

        #layout trello
        self.layout_trello = QHBoxLayout(self.widget_trello)

        #scroll area board
        self.scroll_area_board = QScrollArea()
        self.scroll_area_board.setWidgetResizable(True)
        self.layout_trello.addWidget(self.scroll_area_board)

        #widget board
        self.widget_board = QWidget()
        self.scroll_area_board.setWidget(self.widget_board)

        #layout board
        self.layout_board = QHBoxLayout(self.widget_board)


    def close_project(self):
        self.stacked_widget.setCurrentIndex(self.pages["projects"])


    def update_trello(self):
        # Clear existing widgets
        while self.layout_board.count():
            item = self.layout_board.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.scroll_cols.clear()  # Clear the list of column widgets

        info = sqlite_funcs.get_task_basic_info_by_project_id(self.project_id, "id")
        self.subboard_name = info["subboard_name"]
        task_info = info["task_ids"]

        for subboard_id in self.subboard_name:
            col_widget = ColWidget(title=self.subboard_name[subboard_id])
            self.layout_board.addWidget(col_widget)
            self.scroll_cols.append(col_widget)

            button_add_card = QPushButton("Add Card")
            button_add_card.clicked.connect(self.slot_button_add_card)
            col_widget.layout.addWidget(button_add_card)

            for card in task_info[subboard_id]:
                card_widget = CardWidget(name=card["name"], id=card["id"])
                card_widget.delete_signal.connect(self.delete_card)
                card_widget.open_signal.connect(self.open_card)
                col_widget.layout.addWidget(card_widget)

            col_widget.layout.addStretch()

    def delete_card(self, card_id):
        sqlite_funcs.delete_card(card_id)
        self.update_trello()
    def open_card(self, card_id):
        self.card_window = CardWindow(self, card_id)
        self.card_window.exec()







#slots trello-------------------
    def slot_button_add_column(self):
        self.add_col_window = AddColWindow(self)
        self.add_col_window.exec()

    def slot_button_add_card(self):
        self.add_card_window = AddCardWindow(self)
        self.add_card_window.exec()

    def remove_extra(self, scroll_col: ColWidget):
        layout = scroll_col.layout
        for i in range(layout.count()-1, -1, -1):
            item = layout.itemAt(i)
            if item.spacerItem():
                layout.removeItem(item)

    def create_login_page(self):
        self.central_widget_login = QWidget()
        self.stacked_widget.addWidget(self.central_widget_login)
        self.layout_main_login = QVBoxLayout(self.central_widget_login)


        #label welcome------
        welcome_label = QLabel(self)
        welcome_label.setText("Welcome to Trello")
        self.layout_main_login.addWidget(welcome_label)

        signin_label = QLabel(self)
        signin_label.setText("Login:")
        self.layout_main_login.addWidget(signin_label)

        self.input_username = QLineEdit(self)
        self.input_username.setPlaceholderText("Username")
        self.input_username.setMaxLength(4)
        self.input_username.setMaximumWidth(200)
        validator = QIntValidator()
        validator.setRange(0,9999)
        self.input_username.setValidator(validator)
        self.layout_main_login.addWidget(self.input_username)

        self.input_password = QLineEdit(self)
        self.input_password.setPlaceholderText("Password")
        self.input_password.setMaxLength(40)
        self.input_password.setMaximumWidth(200)
        self.layout_main_login.addWidget(self.input_password)

        signin_button = QPushButton("Sign in")
        signin_button.setMaximumWidth(100)
        signin_button.clicked.connect(self.login_attempt)
        self.layout_main_login.addWidget(signin_button)

        signup_label = QLabel(self)
        signup_label.setText("Sign up:")
        self.layout_main_login.addWidget(signup_label)

        self.input_firstname = QLineEdit(self)
        self.input_firstname.setPlaceholderText("First Name")
        self.input_firstname.setMaxLength(40)
        self.input_firstname.setMaximumWidth(200)
        self.layout_main_login.addWidget(self.input_firstname)

        self.input_lastname = QLineEdit(self)
        self.input_lastname.setPlaceholderText("Last Name")
        self.input_lastname.setMaxLength(40)
        self.input_lastname.setMaximumWidth(200)
        self.layout_main_login.addWidget(self.input_lastname)

        self.input_setpassword = QLineEdit(self)
        self.input_setpassword.setPlaceholderText("Set Password")
        self.input_setpassword.setMaxLength(40)
        self.input_setpassword.setMaximumWidth(200)
        self.layout_main_login.addWidget(self.input_setpassword)

        self.input_email_address = QLineEdit(self)
        self.input_email_address.setPlaceholderText("Email Address")
        self.input_email_address.setMaxLength(40)
        self.input_email_address.setMaximumWidth(200)
        self.layout_main_login.addWidget(self.input_email_address)

        signup_button = QPushButton("Sign up")
        signup_button.setMaximumWidth(100)
        signup_button.clicked.connect(self.signup_attempt)
        self.layout_main_login.addWidget(signup_button)

        #debug stuff---------------------
        debug_label = QLabel(self)
        debug_label.setText("Debug stuff:")
        self.layout_main_login.addWidget(debug_label)

        test_get_button = QPushButton("Test get")
        test_get_button.setMaximumWidth(100)
        test_get_button.clicked.connect(sqlite_funcs.test_get)
        self.layout_main_login.addWidget(test_get_button)

        #push everything before this to the top and everything below to the bottem
        self.layout_main_login.addStretch()

        self.error = QLabel(self)
        self.error.setStyleSheet("color: red")
        self.layout_main_login.addWidget(self.error)

        self.messege = QLabel(self)
        self.messege.setStyleSheet("color: white")
        self.layout_main_login.addWidget(self.messege)

    def login_attempt(self):
        username = self.input_username.text()
        password = self.input_password.text()
        if username == '' or password == '':
            self.error.setText("incorrect username or password")
            return
        if sqlite_funcs.login_check(int(username), password):
            self.username = self.input_username.text()
            self.update_projects_page()
            self.update_projects()
            self.stacked_widget.setCurrentIndex(1)
            with open("username.txt", "w") as f:
                f.write(self.username)
        else:
            self.error.setText("incorrect username or password")

    def signup_attempt(self):
        firstname = self.input_firstname.text()
        lastname = self.input_lastname.text()
        password = self.input_setpassword.text()
        email = self.input_email_address.text()

        if firstname == '' or lastname == '' or password == '' or email == '':
            self.error.setText("all fields are required")
            return
        if sqlite_funcs.signup_check(email):
            username = sqlite_funcs.signup_register(firstname, lastname, password, email)
            self.messege.setText(f"Your 4 digit username is {username}.\nYou can login with your username")

        else:
            self.error.setText("this email address is already used")

    def create_projects_page(self):
        self.central_widget_projects = QWidget()
        self.stacked_widget.addWidget(self.central_widget_projects)
        self.layout_main_projects = QVBoxLayout(self.central_widget_projects)

        self.widget_welcome = QWidget()
        self.layout_main_projects.addWidget(self.widget_welcome)

        self.layout_welcome = QHBoxLayout(self.widget_welcome)

        self.label_welcome = QLabel(self.widget_welcome)
        self.label_welcome.setText(f"Welcome {self.user_data['first name']} {self.user_data['last name']}!")
        self.layout_welcome.addWidget(self.label_welcome)

        self.button_create_project = QPushButton("Create New Project")
        self.button_create_project.setMaximumWidth(200)
        self.button_create_project.clicked.connect(self.create_new_project)
        self.layout_welcome.addWidget(self.button_create_project)

        self.button_user_settings = QPushButton("User Settings")
        self.button_user_settings.setMaximumWidth(200)
        self.button_user_settings.clicked.connect(self.open_user_settings_window)
        self.layout_welcome.addWidget(self.button_user_settings)

        self.button_signout_projects = QPushButton("Sign Out")
        self.button_signout_projects.setMaximumWidth(200)
        self.button_signout_projects.clicked.connect(self.open_login_window)
        self.layout_welcome.addWidget(self.button_signout_projects)

        self.widget_projects = QWidget()
        self.layout_main_projects.addWidget(self.widget_projects)

        self.layout_projects = QHBoxLayout(self.widget_projects)


        #admin projects---------------------------
        self.scroll_area_admin_projects = QScrollArea()
        self.scroll_area_admin_projects.setWidgetResizable(True)
        self.scroll_area_admin_projects.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.layout_projects.addWidget(self.scroll_area_admin_projects)

        self.widget_admin_projects = QWidget()
        self.scroll_area_admin_projects.setWidget(self.widget_admin_projects)

        self.layout_admin_projects = QVBoxLayout(self.widget_admin_projects)

        # leader projects---------------------------
        self.scroll_area_leader_projects = QScrollArea()
        self.scroll_area_leader_projects.setWidgetResizable(True)
        self.scroll_area_leader_projects.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.layout_projects.addWidget(self.scroll_area_leader_projects)

        self.widget_leader_projects = QWidget()
        self.scroll_area_leader_projects.setWidget(self.widget_leader_projects)

        self.layout_leader_projects = QVBoxLayout(self.widget_leader_projects)

        # member projects---------------------------
        self.scroll_area_member_projects = QScrollArea()
        self.scroll_area_member_projects.setWidgetResizable(True)
        self.scroll_area_member_projects.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.layout_projects.addWidget(self.scroll_area_member_projects)

        self.widget_member_projects = QWidget()
        self.scroll_area_member_projects.setWidget(self.widget_member_projects)

        self.layout_member_projects = QVBoxLayout(self.widget_member_projects)







    def update_projects_page(self):
        self.user_data = sqlite_funcs.get_user_data(self.username)
        self.label_welcome.setText(f"Welcome {self.user_data['first name']} {self.user_data['last name']}!")

    def update_projects(self):
        self.projects = sqlite_funcs.get_projects_by_username(self.username)
        layout = QVBoxLayout
        for key in self.projects:
            match key:
                case "admin":
                    layout = self.layout_admin_projects
                case "leader":
                    layout = self.layout_leader_projects
                case "member":
                    layout = self.layout_member_projects

            while layout.count():
                item = layout.takeAt(0)  # Remove the item from the layout
                widget = item.widget()
                if widget is not None and isinstance(widget, ProjectWidget):  # Detach widget from layout and window
                    widget.deleteLater()  # Schedule widget for deletion

        label_admin = QLabel(self)
        label_admin.setText(f"Admin projects")
        self.layout_admin_projects.addWidget(label_admin)

        label_leader = QLabel(self)
        label_leader.setText(f"Leader projects")
        self.layout_leader_projects.addWidget(label_leader)

        label_member = QLabel(self)
        label_member.setText(f"Member projects")
        self.layout_member_projects.addWidget(label_member)

        for key in self.projects:
            for project in self.projects[key]:
                project_data = sqlite_funcs.get_project_data_with_id(project)
                project_widget = ProjectWidget(project, project_data["name"], sqlite_funcs.get_username_with_userid(project_data["leader"]), project_data["first name"], project_data["last name"], project_data["date created"].__str__())
                project_widget.delete_signal.connect(self.delete_project)
                project_widget.open_signal.connect(self.open_project)

                match key:
                    case "admin":
                        self.layout_admin_projects.addWidget(project_widget)
                    case "leader":
                        self.layout_leader_projects.addWidget(project_widget)
                    case "member":
                        self.layout_member_projects.addWidget(project_widget)
        self.layout_admin_projects.addStretch()
        self.layout_leader_projects.addStretch()
        self.layout_member_projects.addStretch()

    def delete_project(self, project_id):
        sqlite_funcs.delete_project(project_id)
        self.update_projects()

    def open_project(self, project_id):
        self.project_id = project_id
        self.update_trello()
        self.stacked_widget.setCurrentIndex(self.pages["trello"])




    def open_user_settings_window(self):
        self.user_settings_window = UserSettingsWindow(self)
        self.user_settings_window.show()

    def open_login_window(self):
        self.stacked_widget.setCurrentIndex(self.pages["login"])
        with open("username.txt", "w") as f:
            pass

    def create_new_project(self):
        self.create_project_window = CreateProjectWindow(self)
        self.create_project_window.exec()
        self.update_projects()

