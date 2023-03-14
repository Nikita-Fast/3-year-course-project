from PySide2.QtCore import QLineF
from PySide2.QtWidgets import QGraphicsLineItem, QGraphicsItem

from typing import TYPE_CHECKING

from validators.port_scene_items_connection_validator import PortSceneItemsConnectionValidator

if TYPE_CHECKING:
    from base.port.port_scene_item import PortSceneItem


class BaseConnectionGraphicsComponent(QGraphicsItem):
    """базовый класс графической компоненты соединения
    его наследники по задумке могут быть чем угодно:
    прямой линией, ломанной, какой-то стрелкой, QGraphicsPathItem и т.д."""
    pass


class ConnectionSceneItemDraft(QGraphicsLineItem):
    """Соединение связывает два порта. Хочется иметь класс с меньшим количеством деталей, чем в прошлых попытках.
    Хочется отвязаться от текущего механизма отрисовки, в котором соединение формируется с помощью
    движения мышью с зажатой левой кнопкой.
    Идея в том, чтобы иметь механизм, передающий со сцены два выбранных порта. Этих двух портов должно быть достаточно
    для любой обработки т.к. порты имеют ссылки на свою сцену и блок в котором они находятся.
    Это позволяет выделить отдельно механизм валидации соединения.
    todo Непонятно можно ли отделить механизм отрисовки соединения,
    С одной стороны мы знаем где на сцене расположены порты, поэтому нарисовать что-то мы можем,
    но что рисовать зависит от базового класса графической компоненты, например
    сейчас это QGraphicsLineItem, а может быть какой-то свой класс
    todo [значит нужен базовый класс графической компоненты соединения, унаследованный, например, от QGraphicsItem]
    todo а если базовый класс унаследовать от QGraphicsPathItem?
    """

    def __init__(self, source_port: "PortSceneItem", dst_port: "PortSceneItem"):
        """Для создания объектов не вызывай конструктор напрямую, а используй отдельный
        @classmethod try_connect_ports
        """
        super().__init__(QLineF(source_port.center_scene_pos(), dst_port.center_scene_pos()))
        self.source = source_port
        self.destination = dst_port

    @classmethod
    def try_connect_ports(cls, source_port: "PortSceneItem", dst_port: "PortSceneItem"):
        """Если переданные порты могут быть корректно соединены, то
        возвращаем новое соединение и сохраняем в портах ссылку на это соединение,
        иначе возвращаем None"""
        if PortSceneItemsConnectionValidator.is_valid(source_port, dst_port):
            obj = cls(source_port, dst_port)
            source_port.connection = obj
            dst_port.connection = obj
            return obj
        else:
            return None

    def update_graphics(self):
        line = QLineF(self.source.center_scene_pos(), self.destination.center_scene_pos())
        self.setLine(line)

    def remove(self):
        if self.source is not None:
            self.source.disconnect()
        if self.destination is not None:
            self.destination.disconnect()
        if self.scene() is not None:
            self.scene().removeItem(self)
