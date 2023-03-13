from PySide2.QtWidgets import QMenuBar, QMenu


class MenuBar(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        modelling_settings = QMenu('Modelling')
        modelling_settings.addAction('Error threshold')
        modelling_settings.addAction('Bit threshold')

        settings = QMenu('Settings')
        settings.addMenu(modelling_settings)
        self.addMenu(settings)

