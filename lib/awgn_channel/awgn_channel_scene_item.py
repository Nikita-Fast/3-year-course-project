from base.block.block_scene_item import BlockSceneItem
from base.port.port_scene_item import PortSceneItem, PortType


class AWGNChannelSceneItem(BlockSceneItem):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.add_input(PortSceneItem(PortType.INPUT_PORT, block=self, number=0), 100)
        self.add_output(PortSceneItem(PortType.OUTPUT_PORT, block=self, number=0), 100)
        self.set_name('AWGN channel')
