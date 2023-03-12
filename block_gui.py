# базовый класс для графического представления блока.
# его задача - взять параметры от пользователя, осуществить их валидацию и передать параметры в реализацию блока
from typing import List

from PySide2.QtWidgets import QWidget


class BlockGUI(QWidget):
    """Класс описывает графический интерфейс блока, открывающийся по двойному клику на блок, расположенный на сцене"""
    # QFormLayout

    def read_params(self, params: List):
        pass

