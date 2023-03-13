# класс описывающий интерфейс сцены на которой производится потсроение модели
from abc import ABC, abstractmethod
from typing import Any

import PySide2
from PySide2.QtCore import Qt
from PySide2.QtGui import QPen, QBrush
from PySide2.QtWidgets import QGraphicsScene, QGraphicsItem, QTreeWidgetItem

from base.base_scene_item import BaseSceneItem
from base.connection_scene_item import ConnectionSceneItem
from base.port_scene_item import PortSceneItem
from validators.connection_scene_item_validator import ConnectionSceneItemValidator


class BaseGraphicsScene(QGraphicsScene):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.curr_connection: ConnectionSceneItem = None
        self.blocks = []

    def mousePressEvent(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            if self.is_port_under_mouse(event):
                port = self.get_port_under_mouse(event)

                if port.is_connected():
                    return
                else:
                    self.curr_connection = ConnectionSceneItem(event.scenePos(), event.scenePos())

                    port.connection = self.curr_connection
                    self.curr_connection.source_port = port

                    self.addItem(self.curr_connection)
                    return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if self.curr_connection is not None:
            self.curr_connection.update_dst_pos(event.scenePos())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if self.curr_connection is not None:
            if self.is_port_under_mouse(event):
                dst_port = self.get_port_under_mouse(event)

                if dst_port.is_connected():
                    self.remove_cur_connection()
                else:
                    dst_port.connection = self.curr_connection
                    self.curr_connection.dst_port = dst_port

                    is_valid = ConnectionSceneItemValidator.is_valid(self.curr_connection)
                    if not is_valid:
                        self.remove_cur_connection()
            else:
                if self.curr_connection is not None:
                    self.remove_cur_connection()

        self.curr_connection = None
        super().mouseReleaseEvent(event)

    def remove_cur_connection(self):
        self.curr_connection.remove_from_ports()
        self.removeItem(self.curr_connection)

    def is_port_under_mouse(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent):
        items = self.items(event.scenePos())
        if len(items) > 0:
            return any(isinstance(item, PortSceneItem) for item in items)
        return False

    def get_port_under_mouse(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent):
        for item in self.items(event.scenePos()):
            if isinstance(item, PortSceneItem):
                return item

    def add_block(self, block: BaseSceneItem):
        """добавить на сцену блок"""
        self.addItem(block)
        self.blocks.append(block)
        pass

    def remove_block(self, block):
        """убрать блок со сцены"""
        self.items().remove(block)
        pass

    def add_connection(self, connection):
        """пусть метод не создает объект connection, а лишь добавляет на сцену уже кем-то созданный, провернный и т.д.
        За корректное создание соединений пусть отвечает кто-то другой, потому что процесс это не простой и
        наверное может иметь несколько вариантов решения
        """
        pass

    def remove_connection(self, connection):
        pass
