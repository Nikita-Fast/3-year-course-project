from base.block.block_scene_item import BlockSceneItem
from lib.ber_calculator.gui import BERCalculatorGUI
from base.port.port_scene_item import PortSceneItem, PortType


class BinaryGeneratorSceneItem(BlockSceneItem):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.add_input(PortSceneItem(PortType.INPUT_PORT, block=self, number=0), 50)
        self.add_input(PortSceneItem(PortType.INPUT_PORT, block=self, number=1), 150)
        self.add_output(PortSceneItem(PortType.OUTPUT_PORT, block=self, number=0), 100)
        self.set_name('BER')

        # todo хочется без агрегации. Действительно ли хочется?
        self.block_gui = BERCalculatorGUI()
