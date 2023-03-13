
class FieldValidator:
    """Предназначен для валидации одного конкретного поля у блока"""
    def __init__(self):
        pass

    def is_valid(self, value) -> bool:
        pass


class IntFieldValidator(FieldValidator):

    def is_valid(self, value) -> bool:
        try:
            v = int(value)
            return True
        except ValueError:
            return False
