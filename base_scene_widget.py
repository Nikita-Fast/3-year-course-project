from PySide2.QtWidgets import QWidget, QGraphicsTextItem


class BaseSceneWidget(QWidget):
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.set_size()
        self.set_name('BaseWidget')

    def set_size(self):
        self.setMinimumSize(200, 200)

    def set_name(self, name: str):
        # name = QGraphicsTextItem(name, self)
        # block_w = self.minimumSize().width()
        # block_h = self.minimumSize().height()
        # _, _, w, h = name.boundingRect().getRect()
        # name.setX(block_w/2 - w/2)
        # name.setY(block_h/2 - h/2)
        pass