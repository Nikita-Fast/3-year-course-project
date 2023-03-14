import uuid
from abc import abstractmethod, ABC

from base.port.port_implementation import PortImplementation


class BlockImplementation(ABC):
    """Базовый класс реализации блоков. По сути это те блоки, которые писали осенью.
    Блок имеет заданное количество портов входных и выходных
    Производный класс определяет их количество и определяет их назначение
    Производный класс сам забирает из них данные и кладет их на выход
    """
    def __init__(self, num_input_ports, num_output_ports):
        self.inputs = [PortImplementation(self, i) for i in range(num_input_ports)]
        self.outputs = [PortImplementation(self, i) for i in range(num_output_ports)]
        # self.config = None
        # self.input_buffer = None
        # self.output_buffer = None
        self.id = uuid.uuid4()

    def execute(self):
        """
        Блоку все равно, что происходит вне него. Он производит обработку данных если данных на входе у него достаточно.
        Скорее всего необходимо сделать общий параметр для блока - размер шага. (а может и не надо - обсудим при встрече)
        """
        input_data_available = True
        for p in self.inputs:
            input_data_available = input_data_available and p.is_data_available()
        if input_data_available:
            self._execute_()

    @abstractmethod
    def _execute_(self):
        """
        Метод определяется производным классом и здесь описывается сама обработка (в том числе надо продумать обратную
        связь с gui для визуализации промежуточных результатов)
        """
        pass

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.id)
