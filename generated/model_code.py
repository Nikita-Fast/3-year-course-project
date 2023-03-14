from lib.binary_generator.binary_generator_implementation import BinaryGeneratorImplementation
from lib.awgn_channel.awgn_channel_implementation import AWGNChannel
from base.connection.connection_implementation import ConnectionImplementation

binarygeneratorimplementation0 = BinaryGeneratorImplementation(bits_num=128, )
awgnchannel0 = AWGNChannel(information_bits_per_symbol=4, ebn0_db=20, )

c0 = ConnectionImplementation(binarygeneratorimplementation0.outputs[0], awgnchannel0.inputs[0])