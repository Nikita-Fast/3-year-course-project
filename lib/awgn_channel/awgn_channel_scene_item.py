from base.base_scene_item import BaseSceneItem
from base.port_scene_item import PortSceneItem, PortType


class AWGNChannelSceneItem(BaseSceneItem):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.add_port(PortSceneItem(PortType.INPUT_PORT, block=self), 0, 100)
        self.add_port(PortSceneItem(PortType.OUTPUT_PORT, block=self), 200, 100)
        self.set_name('AWGN channel')
