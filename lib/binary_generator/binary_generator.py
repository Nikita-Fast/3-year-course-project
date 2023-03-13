from typing import List

from base.block import Block
from utils.field import Field
from utils.field_validator import IntFieldValidator


class BinaryGenerator(Block):
    def __init__(self):
        field = Field('bits_num', int, IntFieldValidator())
        super().__init__([field])

