from base.block.block_description import BlockDescription
from utils.parameter import Parameter
from validators.param_validator import IntParameterValidator


class AWGNChannel(BlockDescription):

    def __init__(self):
        super().__init__([
            Parameter('information_bits_per_symbol', int, IntParameterValidator(), ),
            Parameter('ebn0_db', int, IntParameterValidator())
        ])

