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
    """Описание графической сцены с блоками и соединениями"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.new_connection: ConnectionSceneItem = None
        self.blocks = []

    def mousePressEvent(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            if self.is_port_under_mouse(event):
                self.port_clicked(event)
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if self.new_connection is not None:
            self.new_connection.update_dst_pos(event.scenePos())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if self.new_connection is not None:
            if self.is_port_under_mouse(event):
                dst_port = self.get_port_under_mouse(event)
                self.connect_dst_port(dst_port)
            else:
                self.remove_new_connection()

        self.new_connection = None
        super().mouseReleaseEvent(event)

    def connect_source_port(self, port: PortSceneItem, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent):
        """Создаем соединение исходящее из переданного порта источника"""
        self.new_connection = ConnectionSceneItem(
            event.scenePos(),
            event.scenePos(),
            source_port=port)
        port.connection = self.new_connection

    def port_clicked(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent):
        """Обработка нажатия мышью на порт"""
        port = self.get_port_under_mouse(event)

        if not port.is_connected():
            self.connect_source_port(port, event)
            self.addItem(self.new_connection)

    def connect_dst_port(self, dst_port: PortSceneItem):
        """Пробуем подключить соединение к порту назначения"""
        if dst_port.is_connected():
            self.remove_new_connection()
        else:
            dst_port.connection = self.new_connection
            self.new_connection.dst_port = dst_port

            self.validate_new_connection()

    def validate_new_connection(self):
        """Удаляет только что созданное соединение, если оно не валидно"""
        is_valid = ConnectionSceneItemValidator.is_valid(self.new_connection)
        if not is_valid:
            self.remove_new_connection()

    def remove_new_connection(self):
        """корректное удаление объекта ConnectionSceneItem. Ранее подключенные порты не должны более
        ссылаться на это соединение. Само соединение нужно убрать со сцены"""
        self.new_connection.remove_from_ports()
        self.removeItem(self.new_connection)

    def is_port_under_mouse(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent):
        """Возвращает True, если кликнули мышью по порту"""
        items = self.items(event.scenePos())
        if len(items) > 0:
            return any(isinstance(item, PortSceneItem) for item in items)
        return False

    def get_port_under_mouse(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent):
        """Возвращает порт на который кликнули мышью. Если порты блоков накладываются
        друг на друга, то вернется порты, визуально лежащий на верхнем слое"""
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
