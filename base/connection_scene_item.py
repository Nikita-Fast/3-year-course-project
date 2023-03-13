from PySide2.QtCore import QLineF, QPointF
from PySide2.QtWidgets import QGraphicsLineItem

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.port_scene_item import PortSceneItem


class ConnectionSceneItem(QGraphicsLineItem):

    def __init__(self,
                 source_pos: QPointF,
                 dst_pos: QPointF,
                 source_port: "PortSceneItem" = None,
                 dst_port: "PortSceneItem" = None,
                 parent=None):
        super().__init__(QLineF(source_pos, dst_pos), parent)
        self.source_port = source_port
        self.dst_port = dst_port

    def on_port_changed_scene_position(self):
        source_pos, dst_pos = self.line().p1(), self.line().p2()

        if self.source_port is not None:
            source_pos = self.source_port.center_scene_pos()
        if self.dst_port is not None:
            dst_pos = self.dst_port.center_scene_pos()

        self.setLine(QLineF(source_pos, dst_pos))

    def update_dst_pos(self, dst_pos: QPointF):
        source_pos = self.line().p1()
        self.setLine(QLineF(source_pos, dst_pos))
        
    def remove_from_ports(self):
        if self.source_port is not None:
            self.source_port.connection = None
        if self.dst_port is not None:
            self.dst_port.connection = None
