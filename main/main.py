import sys

from PySide2.QtWidgets import QApplication
from main_window_gui.gui import GUI

app = QApplication([])
window = GUI()
sys.exit(app.exec_())
