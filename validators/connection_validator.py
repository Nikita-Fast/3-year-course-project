from base.connection import Connection


class ConnectionValidator:
    """Объект этого класса проверяет валидно ли соединение"""

    @staticmethod
    def is_valid(connection: Connection) -> bool:
        flag = True
        flag = flag and connection.source.data_type == connection.destination.data_type

        return flag

