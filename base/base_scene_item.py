import PySide2
from PySide2.QtCore import Qt, Signal, QObject
from PySide2.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsTextItem

from base.block_gui import BlockGUI
from base.port import Port


class BaseSceneItem(QGraphicsRectItem):
    """Класс описывает графическое представление блоков на самой сцене"""

    def __init__(self, parent: QGraphicsItem = None):
        super().__init__(parent)

        self.gui: BlockGUI = None
        self.name: QGraphicsTextItem = None

        self.setup_appearance()
        self.set_flags()

    def mouseDoubleClickEvent(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if self.gui is not None:
            self.gui.show()

    def add_gui_object(self, gui_obj: BlockGUI):
        self.gui = gui_obj

    def setup_appearance(self):
        self.set_size()
        self.set_brush()
        self.set_name('BaseItem')

    def set_size(self):
        self.setRect(0, 0, 200, 200)

    def set_flags(self):
        flags = QGraphicsItem.ItemIsMovable | QGraphicsItem.ItemSendsScenePositionChanges
        self.setFlags(flags)

    def set_brush(self):
        self.setBrush(Qt.darkGray)

    def set_name(self, name: str):
        if self.name is None:
            self.name = QGraphicsTextItem(name, self)
        else:
            self.name.setPlainText(name)
        _, _, block_w, block_h = self.boundingRect().getRect()
        _, _, w, h = self.name.boundingRect().getRect()
        self.name.setX(block_w/2 - w/2)
        self.name.setY(block_h/2 - h/2)

    def add_port(self, port: Port, x, y):
        """Пусть расположение портов будет пока задаваться вручную. Параметры
        x, y задают где будет расположен центр порта"""
        port.setParentItem(self)
        _, _, w, h = port.boundingRect().getRect()
        port.setX(x - w/2)
        port.setY(y - h/2)
