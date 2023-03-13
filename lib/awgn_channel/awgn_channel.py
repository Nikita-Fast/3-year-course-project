from base.block import Block
from utils.parameter import Parameter
from validators.param_validator import IntParameterValidator


class AWGNChannel(Block):

    def __init__(self):
        super().__init__([
            Parameter('information_bits_per_symbol', int, IntParameterValidator(), ),
            Parameter('ebn0_db', int, IntParameterValidator())
        ])

