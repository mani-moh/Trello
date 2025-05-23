from PySide6.QtWidgets import QVBoxLayout, QLabel, QMainWindow, QWidget
from PySide6.QtCore import QSize

class UserSettingsWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.min_X = 600
        self.min_Y = 300
        self.setMinimumSize(QSize(self.min_X, self.min_Y))
        self.resize(600, 300)
        self.setWindowTitle("User Settings")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout_main = QVBoxLayout(self.central_widget)

        label_first_name = QLabel(f"First Name: {self.main_window.user_data['first name']}")
        label_last_name = QLabel(f"Last Name: {self.main_window.user_data['last name']}")
        label_email = QLabel(f"Email: {self.main_window.user_data['email']}")
        label_type = QLabel(f"Type: {self.main_window.user_data['type']}")
        label_is_admin = QLabel(f"Admin: {'True' if self.main_window.user_data['is admin'] else 'False'}")
        label_phone_number = QLabel(f"Phone Number: {self.main_window.user_data['phone number']}")
        label_date = QLabel(f"Date Created: {self.main_window.user_data['date created'].__str__()}")
        self.layout_main.addWidget(label_first_name)
        self.layout_main.addWidget(label_last_name)
        self.layout_main.addWidget(label_email)
        self.layout_main.addWidget(label_type)
        self.layout_main.addWidget(label_is_admin)
        self.layout_main.addWidget(label_phone_number)


