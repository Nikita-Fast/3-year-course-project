import uuid

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base.port.port_implementation import PortImplementation


class ConnectionImplementation:
    def __init__(self, port_source: "PortImplementation", port_destination: "PortImplementation"):
        self.source = port_source
        self.destination = port_destination
        self.id = uuid.uuid4()

    def flush(self):
        self.destination.put(self.source.get(len(self.source.buffer)))
