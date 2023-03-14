import uuid
from typing import Any, List

import PySide2
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsTextItem

from base.block.block_gui import BlockGUI
from base.port.port_scene_item import PortSceneItem


class BlockSceneItem(QGraphicsRectItem):
    """Класс описывает графическое представление блоков на самой сцене
    """

    def __init__(self, parent: QGraphicsItem = None):
        super().__init__(parent)
        self.id = uuid.uuid4()

        self.inputs: List[PortSceneItem] = []
        self.outputs: List[PortSceneItem] = []

        self.gui: BlockGUI = None
        self.name: QGraphicsTextItem = None

        self.setup_appearance()
        self.set_flags()

    def get_description(self):
        # todo метод полный отстой?
        return self.gui.block_description

    def mouseDoubleClickEvent(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if self.gui is not None:
            self.gui.show()

    def itemChange(self, change: PySide2.QtWidgets.QGraphicsItem.GraphicsItemChange, value: Any) -> Any:
        if change == QGraphicsItem.ItemScenePositionHasChanged:
            for p in self.inputs + self.outputs:
                p.update_connection_position()
        return super().itemChange(change, value)

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

    # def add_port(self, port: PortSceneItem, x, y):
    #     """Пусть расположение портов будет пока задаваться вручную. Параметры
    #     x, y задают где будет расположен центр порта"""
    #     self.ports.append(port)
    #
    #     port.setParentItem(self)
    #     _, _, w, h = port.boundingRect().getRect()
    #     port.setX(x - w/2)
    #     port.setY(y - h/2)

    def add_input(self, port: PortSceneItem, y):
        """Пусть расположение портов будет пока задаваться вручную. Параметры
        x, y задают где будет расположен центр порта"""
        self.inputs.append(port)

        port.setParentItem(self)
        _, _, w, h = port.boundingRect().getRect()
        port.setX(0 - w/2)
        port.setY(y - h/2)

    def add_output(self, port: PortSceneItem, y):
        """Пусть расположение портов будет пока задаваться вручную. Параметры
        x, y задают где будет расположен центр порта"""
        self.outputs.append(port)

        port.setParentItem(self)
        _, _, w, h = port.boundingRect().getRect()
        _, _, block_w, _ = self.boundingRect().getRect()
        port.setX(block_w - w/2)
        port.setY(y - h/2)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.id)
