from base.block.block_scene_item import BlockSceneItem
from lib.binary_generator.binary_generator_gui import BinaryGeneratorGUI
from base.port.port_scene_item import PortSceneItem, PortType


class BinaryGeneratorSceneItem(BlockSceneItem):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.add_output(PortSceneItem(PortType.OUTPUT_PORT, block=self, number=0), 100)
        self.set_name('Binary generator')

        # todo хочется без агрегации. Действительно ли хочется?
        self.block_gui = BinaryGeneratorGUI()
