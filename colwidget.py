from PySide6.QtWidgets import QWidget, QScrollArea, QSizePolicy, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
import json
from cardwidget import CardWidget

class ColWidget(QScrollArea):
    col_style = "background-color: rgb(30, 30, 30); margin: 5px; padding: 10px;"
    path = "data.json"
    def __init__(self, parent:QWidget=None, title:str = "col"):
        super().__init__(parent)
        self.title = title

        # scroll area extra
        self.setWidgetResizable(True)
        self.setFixedWidth(250)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # widget extra
        self.widget = QWidget()
        self.widget.setStyleSheet(self.col_style)
        self.setWidget(self.widget)

        # layout extra
        self.layout = QVBoxLayout(self.widget)

        self.label = QLabel(self)
        self.label.setText(self.title)
        self.layout.addWidget(self.label)








