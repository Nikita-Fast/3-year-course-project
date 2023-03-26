import uuid

from base.connection.connection_implementation import ConnectionImplementation

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.block.block_implementation import BlockImplementation


class PortImplementation:
    """
    Это класс хранит данные и имеет уникальный номер. Его задача аккумулировать данные.
    Блок берет данные из порта или кладет в него. Здесь есть тонкий момент: предполагается что каждый блок
    на своем входе имеет заданный объем данных (или кратный чему-то).
    """
    def __init__(self, block: "BlockImplementation", number: int, data_type=type):
        self.buffer = []
        self.id = uuid.uuid4()
        self.block = block
        self.number = number
        self.data_type = data_type
        # self.data_portion_size = data_portion_size
        self.connection: ConnectionImplementation = None

    def is_connected(self):
        return self.connection is not None

    def connect(self, connection: ConnectionImplementation):
        self.connection = connection

    def disconnect(self):
        self.connection = None

    def put(self, data: list):
        self.buffer += data

    def get(self, num_elements=None):
        if num_elements is None:
            num_elements = len(self.buffer)
        if len(self.buffer) < num_elements:
            return []
        output = self.buffer[:num_elements]
        self.buffer[:num_elements] = []
        return output

    def is_data_available(self):
        return len(self.buffer) > 0
