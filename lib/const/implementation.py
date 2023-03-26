from base.block.block_implementation import BlockImplementation


class Const(BlockImplementation):

    def __init__(self):
        super().__init__(0, 1)
        self.value = None

    def _execute_(self):
        for p in self.outputs:
            try:
                p.put(self.value)
            except TypeError:
                p.put([self.value])

