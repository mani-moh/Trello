from PySide6.QtWidgets import QApplication
import sys
from mainwindow import MainWindow
import sqlite_funcs

sqlite_funcs.init_db()
app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()