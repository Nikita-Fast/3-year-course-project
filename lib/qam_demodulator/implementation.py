import numpy as np

from base.block.block_implementation import BlockImplementation
from lib.qam_modulator import default_qam_constellations
from lib.qam_modulator.implementation import QAMModulator


class QAMDemodulator(BlockImplementation):

    def __init__(self, bits_per_symbol, constellation=None, mode='hard'):
        super().__init__(1, 1)
        self.bits_per_symbol = bits_per_symbol
        self.constellation = constellation
        self.mode = mode
        if constellation is None:
            self.constellation = default_qam_constellations.get_qam_constellation[bits_per_symbol]

    def _execute_(self):
        data = self.inputs[0].get()

        processed = self.process(np.array(data))
        self.outputs[0].put(list(processed))

    def process(self, data: np.ndarray, noise_variance=None) -> np.ndarray:
        if self.mode == 'hard':
            return self.demodulate_hard(data)
        elif self.mode == 'soft':
            # как посчитать дисперсию шума?
            return self.demodulate_soft(data, noise_variance)
        else:
            raise ValueError("У демодулятора есть только два режима работы: 'hard' и 'soft'")

    @classmethod
    def from_qam_modulator(cls, qam_modulator: QAMModulator, mode='hard'):
        return cls(qam_modulator.bits_per_symbol, qam_modulator.constellation, mode)

    def get_special_constellation_points(self, bit_value, bit_num):
        """Получить точки созвездия, у которых бит с номером bit_num имеет значение равное bit_value"""
        points = []
        for i in range(len(self.constellation)):
            mask = 1 << bit_num
            if i & mask == bit_value << bit_num:
                points.append(self.constellation[i])
        return points

    def _ints_to_bits(self, ints):
        """Конвертирует массив int-ов в их битовое представление, за количество битов, выделяемых
        на каждый int отвечает поле bits_per_symbol."""
        b_len = self.bits_per_symbol
        if b_len > 16:
            raise Exception("Используется модуляция слишком высокого порядка. Поддерживаются только те, что "
                            "кодируют символ числом бит не превосходящим 16")
        if b_len > 8:
            bits = np.unpackbits(ints.astype(">u2").view("u1"))
            mask = np.tile(np.r_[np.zeros(16 - b_len, int), np.ones(b_len, int)], len(ints))
            return bits[np.nonzero(mask)]
        else:
            bits = np.unpackbits(ints.astype(np.uint8))
            mask = np.tile(np.r_[np.zeros(8 - b_len, int), np.ones(b_len, int)], len(ints))
            return bits[np.nonzero(mask)]

    def demodulate_hard(self, symbols):
        c = np.array(self.constellation)

        l = len(symbols)
        idxs = [0]
        acc = 0

        magic_const = 51_200_000 // int(2 ** self.bits_per_symbol)
        while acc < l:
            acc = min(acc + magic_const, l)
            idxs.append(acc)

        n = len(idxs)
        z = zip(idxs[0:n - 1], idxs[1:n])
        pairs = [(i, j) for i, j in z]

        demod_ints = np.empty(l, dtype=int)
        for (a, b) in pairs:
            res = np.abs(symbols[a:b, None] - c[None, :]).argmin(axis=1)
            for i in range(a, b):
                demod_ints[i] = res[i - a]

        demod_bits = self._ints_to_bits(demod_ints)
        return demod_bits
