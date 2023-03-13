import uuid

from base.port import Port


class Connection:
    def __init__(self, port_source: Port, port_destination: Port):
        self.source = port_source
        self.destination = port_destination
        self.id = uuid.uuid4()

    def flush(self):
        self.destination.put(self.source.get(len(self.source.buffer)))
