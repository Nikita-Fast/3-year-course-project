from base.block.block_description import BlockDescription
from utils.parameter import Parameter
from validators.param_validator import IntParameterValidator


class QAMDemodulator(BlockDescription):
    def __init__(self):
        super().__init__([
            Parameter('bits_per_symbol', int, IntParameterValidator())
        ])

