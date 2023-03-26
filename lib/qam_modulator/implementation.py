import numpy as np

from lib.qam_modulator import default_qam_constellations

from base.block.block_implementation import BlockImplementation


def shifting(bit_list):
    out = 0
    for bit in bit_list:
        out = (out << 1) | bit
    return out


def bits_to_ints(bits, bits_per_int):
    i = 0
    symbols = np.empty(len(bits) // bits_per_int, dtype=int)
    k = 0
    while i < len(bits):
        symbols[k] = shifting(bits[i:i + bits_per_int])
        i += bits_per_int
        k += 1
    return symbols


def gray_codes(bits_per_symbol: int):
    if bits_per_symbol % 2 != 0:
        raise Exception("Генерация кодов Грея для нечетного bits_per_symbol ещё не реализована")
    order = 2 ** bits_per_symbol
    codes = []
    for i in range(order):
        codes.append(i ^ (i >> 1))

    length = int(np.sqrt(order))
    for i in range(length):
        if i % 2 == 1:
            start = i * length
            end = (i + 1) * length
            codes[start:end] = codes[start:end][::-1]
    return codes


def sort_constellation_points(complex_numbers):
    return sorted(complex_numbers, key=lambda x: (-x.imag, x.real))


class QAMModulator(BlockImplementation):
    """Класс описывающий КАМ модулятор"""

    def __init__(self, bits_per_symbol: int, constellation=None):
        super().__init__(1, 1)
        self.bits_per_symbol = bits_per_symbol
        self.constellation = constellation
        if constellation is None:
            self.constellation = default_qam_constellations.get_qam_constellation[bits_per_symbol]

    def _execute_(self):
        data_size = len(self.inputs[0].buffer)
        data = self.inputs[0].get(data_size)
        if len(data) % self.bits_per_symbol != 0:
            diff = len(data) % self.bits_per_symbol
            r = self.bits_per_symbol - diff
            data = np.pad(data, (0, r), 'constant')

        ints = bits_to_ints(data, self.bits_per_symbol)
        self.outputs[0].put(list(self.constellation[ints]))
