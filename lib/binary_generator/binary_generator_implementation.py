from base.block.block_implementation import BlockImplementation
import numpy as np


class BinaryGeneratorImplementation(BlockImplementation):

    def __init__(self, bits_num: int):
        super().__init__(0, 2)
        self.bits_num = bits_num

    def _execute_(self):
        data = list(np.random.randint(low=0, high=2, size=self.bits_num))
        self.outputs[0].put(data)
        self.outputs[1].put(data)

