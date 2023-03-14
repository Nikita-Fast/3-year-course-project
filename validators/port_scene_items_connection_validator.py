from typing import TYPE_CHECKING

from base.port_type import PortType

if TYPE_CHECKING:
    from base.port_scene_item import PortSceneItem


def is_ports_free(source: "PortSceneItem", destination: "PortSceneItem"):
    return not source.is_connected() and not destination.is_connected()


def has_2_different_ports(source: "PortSceneItem", destination: "PortSceneItem"):
    # соединено 2 различных порта
    if source is not None and destination is not None:
        return source != destination
    return False


def ports_on_different_blocks(source: "PortSceneItem", destination: "PortSceneItem"):
    # порты находятся на разных блоках
    return source.block != destination.block


def is_from_output_to_input(source: "PortSceneItem", destination: "PortSceneItem"):
    # source_port должен быть OUTPUT, а dst_port - INPUT
    return source.port_type == PortType.OUTPUT_PORT and destination.port_type == PortType.INPUT_PORT


class PortSceneItemsConnectionValidator:

    def __init__(self):
        pass

    @staticmethod
    def is_valid(source: "PortSceneItem", destination: "PortSceneItem") -> bool:
        checks = [is_ports_free, has_2_different_ports, ports_on_different_blocks, is_from_output_to_input]
        return all(f(source, destination) for f in checks)
