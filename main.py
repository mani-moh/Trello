from PySide6.QtWidgets import QApplication
import sys
from mainwindow import MainWindow
import init_db

init_db.init_db()
app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()