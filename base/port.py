from enum import Enum

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGraphicsRectItem


class PortType(Enum):
    INPUT_PORT = 0
    OUTPUT_PORT = 1


class Port(QGraphicsRectItem):

    def __init__(self, port_type: PortType, parent=None):
        super().__init__(parent)

        self.port_type = port_type

        self.set_size()
        self.set_brush()

    def set_size(self):
        self.setRect(0, 0, 40, 40)

    def set_brush(self):
        self.setBrush(Qt.red)
