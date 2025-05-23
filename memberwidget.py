from PySide6.QtWidgets import QPushButton, QLabel, QHBoxLayout, QSizePolicy, QFrame

class MemberWidget(QFrame):
    cards_style = "background-color: rgb(50, 50, 50); margin: 5px; padding: 10px; border-radius: 5px; border: 1px solid white"

    def __init__(self, username, first_name, last_name):
        super().__init__()
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.setup_ui()

    def setup_ui(self):
        self.setFixedHeight(70)

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

        #username
        self.label_username = QLabel(self)
        self.label_username.setText(f"{self.username}    {self.first_name} {self.last_name}")
        self.label_username.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.label_username.setWordWrap(True)
        self.layout.addWidget(self.label_username)

        self.delete_button = QPushButton("X", self)
        self.delete_button.setFixedSize(25, 25)
        self.delete_button.clicked.connect(self.delete_card)
        self.layout.addWidget(self.delete_button)

    def delete_card(self):
        self.deleteLater()

