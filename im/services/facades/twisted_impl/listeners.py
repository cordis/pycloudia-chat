from twisted.internet.error import CannotListenError

from im.services.facades.interfaces import IListener
from im.services.facades.exceptions import ListenFailedError


class TcpListener(IListener):
    """
    :type logger: L{ILogger}
    :type reactor: L{from twisted.internet.interfaces.IReactorTCP}
    :type protocol_factory: C{Callable}
    """
    logger = None
    reactor = None
    protocol_factory = None

    def __init__(self, host, min_port=8091, max_port=8094):
        self.host = host
        self.port = None
        self.min_port = min_port
        self.max_port = max_port

    def start(self, director):
        protocol = self.protocol_factory(director)
        for port in range(self.min_port, self.max_port + 1):
            try:
                self.reactor.listenTCP(port, protocol, interface=self.host)
                self.logger.info('Listening started on %s:%s', self.host, port)
            except CannotListenError as e:
                self.logger.info('Listening failed on %s:%s -- %s', self.host, port, e.socketError)
            else:
                self.port = port
        raise ListenFailedError(self.host, (self.max_port, self.max_port))
