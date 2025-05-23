
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QScrollArea, \
    QHBoxLayout, QStackedWidget, QLineEdit
from cardwidget import CardWidget
from colwidget import ColWidget
import sqlite_funcs


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


        #central widget
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        pages = {
            "login": 0,
            "projects": 1,
            "trello" : 2
        }

        self.create_login_page()
        #self.create_projects_page()
        self.create_trello_page()
        self.stacked_widget.setCurrentIndex(0)

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


#slots trello-------------------
    def slot_button_add_column(self):
        scroll_area_col = ColWidget()
        self.layout_board.addWidget(scroll_area_col)



        #add to list

        self.scroll_cols.append(scroll_area_col)

    def slot_button_add_card(self):
        for scroll_col in self.scroll_cols:
            self.remove_extra(scroll_col)

            card = CardWidget(f"name {self.num}", "")


            scroll_col.layout.addWidget(card)
            scroll_col.layout.addStretch()
            self.num += 1

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
            self.username = self.input_username
            self.stacked_widget.setCurrentIndex(1)
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
        if sqlite_funcs.signup_check(firstname, lastname, password, email):
            username = sqlite_funcs.signup_register(firstname, lastname, password, email)
            self.messege.setText(f"Your 4 digit username is {username}.\nYou can login with your username")

        else:
            self.error.setText("this email address is already used")

    def create_prpjects_page(self):
        self.central_widget_projects = QWidget()
        self.stacked_widget.addWidget(self.central_widget_projects)
        self.layout_main_projects = QVBoxLayout(self.central_widget_projects)