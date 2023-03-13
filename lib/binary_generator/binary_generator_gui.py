from PySide2.QtWidgets import QLineEdit

from base.block import Block
from base.block_gui import BlockGUI
from utils.field import Field
from utils.field_validator import IntFieldValidator


class BinaryGeneratorGUI(BlockGUI):

    def __init__(self, parent=None):
        super().__init__(parent)

