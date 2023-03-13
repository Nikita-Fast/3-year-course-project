from PySide2.QtWidgets import QMenuBar


class MenuBar(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.addAction('Model settings')

