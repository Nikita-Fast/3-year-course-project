from base.block.block_scene_item import BlockSceneItem
from lib.const.gui import ConstGUI
from base.port.port_scene_item import PortSceneItem, PortType


class ConstSceneItem(BlockSceneItem):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.add_output(PortSceneItem(PortType.OUTPUT_PORT, block=self, number=0), 100)
        self.set_name('Ebn0_db')

        # todo хочется без агрегации. Действительно ли хочется?
        self.block_gui = ConstGUI()
