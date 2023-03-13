# класс описывающий интерфейс сцены на которой производится потсроение модели
from abc import ABC, abstractmethod
from typing import Any

from PySide2.QtCore import Qt
from PySide2.QtGui import QPen, QBrush
from PySide2.QtWidgets import QGraphicsScene, QGraphicsItem, QTreeWidgetItem

from base.base_scene_item import BaseSceneItem


class BaseGraphicsScene(QGraphicsScene):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.blocks = []

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
