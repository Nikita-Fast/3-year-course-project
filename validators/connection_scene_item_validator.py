from base.connection_scene_item import ConnectionSceneItem
from base.port_scene_item import PortType


def has_2_different_ports(obj: ConnectionSceneItem):
    # соединено 2 различных порта
    if obj.source_port is not None and obj.dst_port is not None:
        return obj.source_port != obj.dst_port
    return False


def ports_on_different_blocks(obj: ConnectionSceneItem):
    # порты находятся на разных блоках
    return obj.source_port.block != obj.dst_port.block


def is_from_output_to_input(obj: ConnectionSceneItem):
    # source_port должен быть OUTPUT, а dst_port - INPUT
    return obj.source_port.port_type == PortType.OUTPUT_PORT and obj.dst_port.port_type == PortType.INPUT_PORT


class ConnectionSceneItemValidator:

    def __init__(self):
        pass

    @staticmethod
    def is_valid(obj: ConnectionSceneItem) -> bool:
        checks = [has_2_different_ports, ports_on_different_blocks, is_from_output_to_input]
        return all(f(obj) for f in checks)
