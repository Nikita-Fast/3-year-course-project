import uuid

import PySide2
from PySide2.QtCore import Qt, QPointF
from PySide2.QtGui import QPen
from PySide2.QtWidgets import QGraphicsRectItem

from base.connection.connection_scene_item import ConnectionSceneItemDraft

from typing import TYPE_CHECKING

from base.port.port_type import PortType

if TYPE_CHECKING:
    from base.block.block_scene_item import BlockSceneItem


class PortSceneItem(QGraphicsRectItem):

    def __init__(self, port_type: PortType, block: "BlockSceneItem", number: int, parent=None):
        super().__init__(parent)
        self.id = uuid.uuid4()
        self.block: "BlockSceneItem" = block
        self.connection: ConnectionSceneItemDraft = None

        self.port_type = port_type

        self.set_size()
        self.set_brush()
        self.setAcceptHoverEvents(True)
        self.number = number

    def is_connected(self):
        return self.connection is not None

    def disconnect(self):
        self.connection = None

    def enable_highlight(self):
        self.setAcceptHoverEvents(False)
        self.setPen(QPen(Qt.green, 3))

    def disable_highlight(self):
        self.setAcceptHoverEvents(True)
        self.setPen(QPen(Qt.black))

    def hoverEnterEvent(self, event: PySide2.QtWidgets.QGraphicsSceneHoverEvent) -> None:
        self.setPen(QPen(Qt.green, 3))

    def hoverLeaveEvent(self, event: PySide2.QtWidgets.QGraphicsSceneHoverEvent) -> None:
        self.setPen(QPen(Qt.black))

    def update_connection_position(self):
        if self.connection is not None:
            self.connection.update_graphics()

    def center_scene_pos(self):
        _, _, w, h = self.rect().getRect()
        return self.scenePos() + QPointF(w/2, h/2)

    def set_size(self):
        self.setRect(0, 0, 40, 40)

    def set_brush(self):
        self.setBrush(Qt.red)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.id)
