from typing import List

from base.block.block_description import BlockDescription
from base.connection.connection_implementation import ConnectionImplementation


class Model:

    def __init__(self):
        self.blocks: List[BlockDescription] = []
        # нужен ли?
        self.connections: List[ConnectionImplementation] = []
