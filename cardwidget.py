from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QPushButton, QLabel, QHBoxLayout, QSizePolicy, QFrame, QMenu


class CardWidget(QFrame):
    cards_style = "background-color: rgb(50, 50, 50); margin: 5px; padding: 10px; border-radius: 5px; border: 1px solid white"
    button_style = '''
        QPushButton {
        background-color: darkred;
        padding: 0px;
        margin: 0px;
        border: none;
        }
        QPushButton:hover {
        background-color: red;
        }
    '''
    delete_signal = Signal(int)
    open_signal = Signal(int)
    def __init__(self, id, name):
        super().__init__()
        self.id = id
        self.name = name
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
                    
                """)

        #main layout
        self.layout = QHBoxLayout(self)

        #title
        self.label = QLabel(self.name, self)
        self.label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)

        # self.delete_button = QPushButton("X", self)
        # self.delete_button.setStyleSheet(self.button_style)
        # self.delete_button.setFixedSize(25, 25)
        # self.delete_button.clicked.connect(self.delete_card)
        # self.layout.addWidget(self.delete_button)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_menu)


    def show_menu(self, pos):
        menu = QMenu(self)
        menu.addAction("Delete Card", self.delete_card)
        menu.addAction("Open", self.open_card)
        menu.exec(self.mapToGlobal(pos))

    def delete_card(self):
        # result = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this card?",
        #                               QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        #                               QMessageBox.StandardButton.No)
        # if result == QMessageBox.StandardButton.Yes:
        #    self.delete_signal.emit(self.id)
        self.delete_signal.emit(self.id)

    def open_card(self):
        self.open_signal.emit(self.id)


