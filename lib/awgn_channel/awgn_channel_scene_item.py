from base.base_scene_item import BaseSceneItem
from base.port import Port, PortType


class AWGNChannelSceneItem(BaseSceneItem):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.add_port(Port(PortType.INPUT_PORT), 0, 100)
        self.add_port(Port(PortType.OUTPUT_PORT), 200, 100)
        self.set_name('AWGN channel')