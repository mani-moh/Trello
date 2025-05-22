from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QScrollArea, \
    QHBoxLayout, QSizePolicy
import json
from cardwidget import CardWidget
from Customwidget import CustomWidget
from colwidget import ColWidget


class MainWindow(QMainWindow):
    cards_style = "background-color: rgb(50, 50, 50); margin: 5px; padding: 10px; border-radius: 5px; border: 1px solid white"
    col_style = "background-color: rgb(30, 30, 30); margin: 5px; padding: 10px;"
    def __init__ (self):
        super().__init__()
        self.path = "data.json"


        self.min_X = 600
        self.min_Y = 300
        self.setMinimumSize(QSize(self.min_X,self.min_Y))
        self.setWindowTitle("Trello")
        self.scroll_cols = []
        self.num = 1




        #central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        #main layout v
        self.layout_main = QVBoxLayout(self.central_widget)

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










    #slots-------------------
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

