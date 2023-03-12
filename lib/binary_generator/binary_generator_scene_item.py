from base_scene_item import BaseSceneItem
from port import Port, PortType


class BinaryGeneratorSceneItem(BaseSceneItem):

    def __init__(self, parent=None):
        super().__init__(parent)

        print('created instance of BinaryGeneratorSceneItem class')

        self.add_port(Port(PortType.OUTPUT_PORT), 200, 100)
        self.set_name('Binary generator')

