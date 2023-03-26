import uuid

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.port.port_implementation import PortImplementation


class ConnectionImplementation:
    def __init__(self, port_source: "PortImplementation", port_destination: "PortImplementation"):
        self.source = port_source
        self.destination = port_destination
        self.id = uuid.uuid4()
        # todo ошибка ли делать так?
        self.source.connect(self)
        self.destination.connect(self)

    def flush(self):
        all_data = self.source.get(len(self.source.buffer))
        self.destination.put(all_data)
