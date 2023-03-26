from base.block.block_implementation import BlockImplementation


class Accumulator(BlockImplementation):

    def __init__(self):
        super().__init__(1, 0)
        self.acc = []

    def _execute_(self):
        data = self.inputs[0].get()
        self.acc += data
