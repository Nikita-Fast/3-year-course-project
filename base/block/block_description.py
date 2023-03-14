
from typing import List, Dict

from utils.parameter import Parameter


class BlockDescription:
    """
    базовый класс описания блока
    задачи: принять параметры от GUI, помочь с их валидацией и сохранить валидные параметры внутри себя.
    Передать сохраненные параметры в кодогенератор
    """
    params: Dict[str, Parameter]

    def __init__(self, fields: List[Parameter]):
        self.params = {field.name: field for field in fields}

    def get_params(self):
        return list(self.params.values())

    def is_each_field_has_valid_value(self) -> bool:
        """Возвращает True, если все поля имеют валидное значение"""
        return all(f.has_valid_data() for f in self.params.values())

    def get_param_names(self):
        """Возвращает список с именами всех полей. Можно использовать для создания формы на GUI блоке"""
        return list(self.params.keys())

    def receive_param_value_from_gui(self, field_name: str, value) -> bool:
        """Метод получает значение поля от gui, валидирует его, если значение прошло валидацию,
        то оно сохраняется. Метод возвращает флаг, указывающий на то, прошло значение валидацию или нет"""
        if field_name in self.params:
            status = self.params[field_name].try_set_data(value)
            print('validation')
            return status
        else:
            raise Exception('Блок не имеет поля с именем %s' % field_name)
