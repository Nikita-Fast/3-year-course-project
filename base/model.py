import uuid
from typing import Dict, List

from base.block import Block
from base.connection import Connection


class Model:

    def __init__(self):
        self.blocks: List[Block] = []
        # uuid порта сопоставляется с соединением
        self.connections: Dict[uuid, Connection] = {}
