from base.block.block_implementation import BlockImplementation


class BERCalculator(BlockImplementation):

    def __init__(self):
        super().__init__(2, 1)

    def _execute_(self):
        tx = self.inputs[0].get()
        rx = self.inputs[1].get()
        if len(tx) != len(tx):
            raise ValueError(
                'Битов отправлено: {}, Битов получено: {}. Количество должно быть равным!'.format(len(tx), len(rx))
            )
        bit_errors = 0
        for i in range(len(tx)):
            if tx[i] != rx[i]:
                bit_errors += 1

        ber = bit_errors / len(tx)
        print('BER = {}'.format(ber))
        self.outputs[0].put([ber])
