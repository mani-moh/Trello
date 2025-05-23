from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton, QLabel, QHBoxLayout, QSizePolicy, QFrame, QMessageBox


class ProjectWidget(QFrame):
    cards_style = "background-color: rgb(50, 50, 50); margin: 5px; padding: 10px; border-radius: 5px; border: 1px solid white"
    delete_signal = Signal(int)
    open_signal = Signal(int)
    def __init__(self, id, name, leader_id, first_name, last_name, date_created):
        super().__init__()
        self.id = id
        self.name = name
        self.leader_id = leader_id
        self.first_name = first_name
        self.last_name = last_name
        self.date_created = date_created
        self.setup_ui()

    def setup_ui(self):
        self.setFixedHeight(100)

        self.setAutoFillBackground(True)
        self.setObjectName("CardWidget")
        self.setStyleSheet("""
                    QFrame {
                        background-color: rgb(50, 50, 50);
                        margin: 5px;
                        padding: 10px;
                        border: 1px solid white;
                        border-radius: 5px;
                    }
                    QLabel {
                        padding: 0px;
                        margin: 0px;
                        border: none;
                    }
                    QPushButton {
                        background-color: darkred;
                        padding: 0px;
                        margin: 0px;
                        border: none;
                    }
                    QPushButton:hover {
                    background-color: red;
                    }
                """)

        #main layout
        self.layout = QHBoxLayout(self)

        #name
        self.label_name = QLabel(self)
        self.label_name.setText(f"{self.name}    ID:{self.id}    Made by: {self.first_name} {self.last_name}({self.leader_id})  At: {self.date_created}")
        self.label_name.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.label_name.setMaximumWidth(200)
        self.label_name.setWordWrap(True)
        self.layout.addWidget(self.label_name)

        self.open_button = QPushButton("O", self)
        self.open_button.setFixedSize(25, 25)
        self.open_button.setStyleSheet('''
        QPushButton {
                        background-color: darkblue;
                        padding: 0px;
                        margin: 0px;
                        border: none;
                    }
        QPushButton:hover {
        background-color: blue;
        }
        ''')
        self.open_button.clicked.connect(self.open_project)
        self.layout.addWidget(self.open_button)

        self.delete_button = QPushButton("X", self)
        self.delete_button.setFixedSize(25, 25)
        self.delete_button.clicked.connect(self.delete_card)
        self.layout.addWidget(self.delete_button)

    def delete_card(self):
        result = QMessageBox.question(self, "Confirm Delete","Are you sure you want to delete this project?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No )
        if result == QMessageBox.StandardButton.Yes:
            self.delete_signal.emit(self.id)

    def open_project(self):
        self.open_signal.emit(self.id)