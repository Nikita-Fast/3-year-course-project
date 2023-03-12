# базовый класс реализации блока
# задачи: принять параметры от GUI, помочь с их валидацией и сохранить валидные параметры внутри себя
# далее когда все блоки сохранили параметры, то можно будет генерировать код на выбранном языке
from abc import ABC, abstractmethod
from typing import List


class Block(ABC):

    @abstractmethod
    def validate_params(self, params: List) -> bool:
        """вернуть True, если переданные параметры прошли валидацию"""
        pass

    @abstractmethod
    def save_params(self, params: List):
        pass
