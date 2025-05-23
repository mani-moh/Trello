from PySide6.QtCore import Signal
from PySide6.QtWidgets import QPushButton, QLabel, QHBoxLayout, QSizePolicy, QWidget, QFrame

class CardWidget(QFrame):
    cards_style = "background-color: rgb(50, 50, 50); margin: 5px; padding: 10px; border-radius: 5px; border: 1px solid white"

    def __init__(self, title, desc):
        super().__init__()
        self.title = title
        self.desc = desc
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

        #title
        self.label = QLabel(self.title, self)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)

        self.delete_button = QPushButton("X", self)
        self.delete_button.setFixedSize(25, 25)
        self.delete_button.clicked.connect(self.delete_card)
        self.layout.addWidget(self.delete_button)

    def delete_card(self):
        self.deleteLater()

