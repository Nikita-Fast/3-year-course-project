from typing import List

import PySide2
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGraphicsScene

from base.block.block_scene_item import BlockSceneItem
from base.connection.connection_scene_item import ConnectionSceneItemDraft
from base.port.port_scene_item import PortSceneItem


class BaseGraphicsScene(QGraphicsScene):
    """Описание графической сцены с блоками и соединениями"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.blocks: List[BlockSceneItem] = []
        self.connections: List[ConnectionSceneItemDraft] = []
        self.clicked_port: PortSceneItem = None

    def mousePressEvent(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            if self.is_port_clicked(event):
                self.port_clicked(event)
                return
            else:
                self.flush_clicked_port()

        super().mousePressEvent(event)

    def port_clicked(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent):
        """Обработка нажатия мышью на порт"""
        port = self.get_port_under_mouse(event)

        if self.clicked_port is None:
            self.clicked_port = port
            port.enable_highlight()
        else:
            self.try_connect_two_ports(self.clicked_port, port)
            self.flush_clicked_port()

    def try_connect_two_ports(self, src: PortSceneItem, dst: PortSceneItem):
        """Пытаемся создать валидный графический объект соединения двух переданных блоков.
        То как два порта были выбраны это отдельный механизм"""
        new_connection = ConnectionSceneItemDraft.try_connect_ports(src, dst)
        if new_connection is not None:
            self.add_connection(new_connection)

    def flush_clicked_port(self):
        if self.clicked_port is not None:
            self.clicked_port.disable_highlight()
        self.clicked_port = None

    def is_port_clicked(self, event: PySide2.QtWidgets.QGraphicsSceneMouseEvent):
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

    def add_block(self, block: BlockSceneItem):
        """добавить на сцену блок"""
        self.addItem(block)
        self.blocks.append(block)
        pass

    def remove_block(self, block):
        """убрать блок со сцены"""
        self.blocks.remove(block)
        self.items().remove(block)
        pass

    def add_connection(self, connection: ConnectionSceneItemDraft):
        """пусть метод не создает объект connection, а лишь добавляет на сцену уже кем-то созданный, провернный и т.д.
        За корректное создание соединений пусть отвечает кто-то другой, потому что процесс это не простой и
        наверное может иметь несколько вариантов решения
        """
        self.connections.append(connection)
        self.addItem(connection)

    def remove_connection(self, connection: ConnectionSceneItemDraft):
        self.connections.remove(connection)
        connection.remove()

    def is_all_blocks_hava_valid_params(self):
        return all(b.get_description().is_each_field_has_valid_value() for b in self.blocks)

    def pass_blocks_and_params(self):
        blocks = self.blocks
        params = []
        for b in self.blocks:
            block_params = b.get_description().get_params()
            params.append(block_params)
        return blocks, params
