import sys

from PySide2.QtWidgets import QApplication

from gui import GUI

app = QApplication([])
window = GUI()
sys.exit(app.exec_())