from validators.param_validator import ParameterValidator


class Parameter:
    """Класс описывает поле. У него есть: имя, тип данных, данные, валидатор.
    """
    def __init__(self, name: str, data_type: type, validator: ParameterValidator, data=None):
        self.name = name
        self.data_type = data_type
        self.data = data
        self.validator = validator

    def try_set_data(self, new_data) -> bool:
        """Если переданное значение валидно, то сохраняем его.
        Возвращаем True, если значение было сохранено.
        """
        if self.validator.is_valid(new_data):
            self.data = new_data
            return True
        else:
            self.data = None
            return False

    def has_valid_data(self):
        return self.data is not None
