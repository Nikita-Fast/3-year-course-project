from typing import List

from base.block import Block
from utils.parameter import Parameter
from validators.param_validator import IntParameterValidator


class BinaryGenerator(Block):
    def __init__(self):
        field = Parameter('bits_num', int, IntParameterValidator())
        super().__init__([field])

