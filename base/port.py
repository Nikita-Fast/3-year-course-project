import uuid


class Port:
    """
    Это класс хранит данные и имеет уникальный номер. Его задача аккумулировать данные.
    Блок берет данные из порта или кладет в него. Здесь есть тонкий момент: предполагается что каждый блок
    на своем входе имеет заданный объем данных (или кратный чему-то).
    """
    def __init__(self, data_portion_size: int, data_type=type):
        self.buffer = []
        self.id = uuid.uuid4()

        self.data_type = data_type
        self.data_portion_size = data_portion_size

    def put(self, data: list):
        self.buffer += data

    def get(self, num_elements):
        if len(self.buffer) < num_elements:
            return []
        output = self.buffer[:num_elements]
        self.buffer[:num_elements] = []
        return output

    def is_data_available(self):
        return len(self.buffer) > 0
