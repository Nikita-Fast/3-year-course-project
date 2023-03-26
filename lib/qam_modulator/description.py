from base.block.block_description import BlockDescription
from utils.parameter import Parameter
from validators.param_validator import IntParameterValidator


class BinaryGenerator(BlockDescription):
    def __init__(self):
        field = Parameter('bits_per_symbol', int, IntParameterValidator())
        super().__init__([field])

