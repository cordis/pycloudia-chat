class Server(object):
    stream_factory = None
    client_factory = None

    def __init__(self, protocol_factory, host, port=None):
        self.protocol_factory = protocol_factory
        self.host = host
        self.port = port
        self.clients = {}
        self.timeouts = {}

    def start(self):
        router = self.stream_factory.create_router_stream()
        router.message_received.connect(self._read_message)
        if self.port is None:
            self.port = router.start_on_random_port(self.host)
        elif isinstance(self.port, (tuple, list)):
            min_port, max_port = self.port
            self.port = router.start_on_random_port(self.host, min_port, max_port)
        else:
            router.start(self.host, self.port)

    def _read_message(self, message):
        if message == self.protocol_factory.CONNECT:
            client = self.clients[message.peer] = self.client_factory(message.peer)
            client.connection_made()
            return

        try:
            client = self.clients[message.peer]
        except KeyError:
            return

        if message == self.protocol_factory.DISCONNECT:
            client.connection_lost()
            return

        client.string_received(message)
