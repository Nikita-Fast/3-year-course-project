from matplotlib import pyplot as plt
from lib.accumulator.implementation import Accumulator
from lib.awgn_channel.awgn_channel_implementation import AWGNChannel
from lib.const.implementation import Const
from lib.binary_generator.binary_generator_implementation import BinaryGeneratorImplementation
from lib.qam_modulator.implementation import QAMModulator
from lib.ber_calculator.implementation import BERCalculator
from lib.qam_demodulator.implementation import QAMDemodulator
from base.connection.connection_implementation import ConnectionImplementation

accumulator0 = Accumulator()
awgnchannel0 = AWGNChannel(information_bits_per_symbol=2, )
const0 = Const()
binarygeneratorimplementation0 = BinaryGeneratorImplementation(bits_num=512000, )
qammodulator0 = QAMModulator(bits_per_symbol=2, )
bercalculator0 = BERCalculator()
qamdemodulator0 = QAMDemodulator(bits_per_symbol=2, )
blocks = [accumulator0, awgnchannel0, const0, binarygeneratorimplementation0, qammodulator0, bercalculator0, qamdemodulator0]

c0 = ConnectionImplementation(bercalculator0.outputs[0], accumulator0.inputs[0])
c1 = ConnectionImplementation(qammodulator0.outputs[0], awgnchannel0.inputs[0])
c2 = ConnectionImplementation(const0.outputs[0], awgnchannel0.inputs[1])
c3 = ConnectionImplementation(awgnchannel0.outputs[0], qamdemodulator0.inputs[0])
c4 = ConnectionImplementation(binarygeneratorimplementation0.outputs[0], bercalculator0.inputs[0])
c5 = ConnectionImplementation(binarygeneratorimplementation0.outputs[1], qammodulator0.inputs[0])
c6 = ConnectionImplementation(qamdemodulator0.outputs[0], bercalculator0.inputs[1])

ebn0_max = 10
for ebn0 in range(ebn0_max):
	const0.value = ebn0
	
	front = set()
	for b in blocks:
		if b.is_source_block():
			front.add(b)
		else:
			pass
	
	while True:
		new_front = set()
		for b in front:
			b.execute()
			new_front.update(b.get_children())
		if new_front:
			front = new_front
		else:
			break

plt.yscale("log")
plt.grid(visible='true')
plt.xlabel("Eb/N0, dB")
plt.ylabel("BER")
plt.plot(accumulator0.acc, '--o', label='QAM-4')
plt.legend()
plt.show()