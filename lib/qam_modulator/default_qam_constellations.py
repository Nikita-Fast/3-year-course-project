import numpy as np

qam_2_symbols = [(-1 + 0j), (1 + 0j)]
qam_4_symbols = [(-1 + 1j), (1 + 1j), (-1 - 1j), (1 - 1j)]
qam_8_symbols = [(-3 + 1j), (-1 + 1j), (1 + 1j), (3 + 1j), (-3 - 1j), (-1 - 1j), (1 - 1j), (3 - 1j)]
qam_16_symbols = [(-3 + 3j), (-1 + 3j), (1 + 3j), (3 + 3j), (-3 + 1j), (-1 + 1j), (1 + 1j), (3 + 1j), (-3 - 1j),
                  (-1 - 1j), (1 - 1j), (3 - 1j), (-3 - 3j), (-1 - 3j), (1 - 3j), (3 - 3j)]
qam_32_symbols = [(-3 + 5j), (-1 + 5j), (1 + 5j), (3 + 5j), (-5 + 3j), (-3 + 3j), (-1 + 3j), (1 + 3j), (3 + 3j),
                  (5 + 3j), (-5 + 1j), (-3 + 1j), (-1 + 1j), (1 + 1j), (3 + 1j), (5 + 1j), (-5 - 1j), (-3 - 1j),
                  (-1 - 1j), (1 - 1j), (3 - 1j), (5 - 1j), (-5 - 3j), (-3 - 3j), (-1 - 3j), (1 - 3j), (3 - 3j),
                  (5 - 3j), (-3 - 5j), (-1 - 5j), (1 - 5j), (3 - 5j)]
qam_64_symbols = [(-7 + 7j), (-5 + 7j), (-3 + 7j), (-1 + 7j), (1 + 7j), (3 + 7j), (5 + 7j), (7 + 7j), (-7 + 5j),
                  (-5 + 5j), (-3 + 5j), (-1 + 5j), (1 + 5j), (3 + 5j), (5 + 5j), (7 + 5j), (-7 + 3j), (-5 + 3j),
                  (-3 + 3j), (-1 + 3j), (1 + 3j), (3 + 3j), (5 + 3j), (7 + 3j), (-7 + 1j), (-5 + 1j), (-3 + 1j),
                  (-1 + 1j), (1 + 1j), (3 + 1j), (5 + 1j), (7 + 1j), (-7 - 1j), (-5 - 1j), (-3 - 1j), (-1 - 1j),
                  (1 - 1j), (3 - 1j), (5 - 1j), (7 - 1j), (-7 - 3j), (-5 - 3j), (-3 - 3j), (-1 - 3j), (1 - 3j),
                  (3 - 3j), (5 - 3j), (7 - 3j), (-7 - 5j), (-5 - 5j), (-3 - 5j), (-1 - 5j), (1 - 5j), (3 - 5j),
                  (5 - 5j), (7 - 5j), (-7 - 7j), (-5 - 7j), (-3 - 7j), (-1 - 7j), (1 - 7j), (3 - 7j), (5 - 7j),
                  (7 - 7j)]

get_qam_constellation = {
    1: np.array(qam_2_symbols),
    2: np.array(qam_4_symbols),
    3: np.array(qam_8_symbols),
    4: np.array(qam_16_symbols),
    5: np.array(qam_32_symbols),
    6: np.array(qam_64_symbols)
}