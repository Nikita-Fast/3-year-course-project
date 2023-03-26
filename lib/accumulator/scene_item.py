from base.block.block_scene_item import BlockSceneItem
from lib.accumulator.gui import AccumulatorGUI
from base.port.port_scene_item import PortSceneItem, PortType


class AccumulatorItem(BlockSceneItem):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.add_input(PortSceneItem(PortType.INPUT_PORT, block=self, number=0), 100)
        self.set_name('Accumulator')

        # todo хочется без агрегации. Действительно ли хочется?
        self.block_gui = AccumulatorGUI()
