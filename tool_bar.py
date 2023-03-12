from PySide2.QtCore import Qt
from PySide2.QtWidgets import QToolBar


class ToolBar(QToolBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAllowedAreas(Qt.TopToolBarArea)

        self.addAction('пыщ')
        self.addAction('start')
        self.addAction('pause')
        self.addAction('step')
        self.addAction('save model')
        self.addAction('open model')

