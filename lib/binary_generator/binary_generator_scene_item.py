from base.base_scene_item import BaseSceneItem
from lib.binary_generator.binary_generator_gui import BinaryGeneratorGUI
from base.port_scene_item import PortSceneItem, PortType


class BinaryGeneratorSceneItem(BaseSceneItem):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.add_port(PortSceneItem(PortType.OUTPUT_PORT, block=self), 200, 100)
        self.set_name('Binary generator')

        # todo хочется без агрегации. Действительно ли хочется?
        self.block_gui = BinaryGeneratorGUI()
