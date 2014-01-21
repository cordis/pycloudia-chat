from twisted.protocols.basic import NetstringReceiver
from twisted.internet.protocol import Factory, connectionDone

from im.services.facades.interfaces import IClient


class Protocol(NetstringReceiver, IClient):
    factory = None

    def connectionMade(self):
        self.factory.connection_made(self)

    def connectionLost(self, reason=connectionDone):
        if self.brokenPeer or reason is not connectionDone:
            self.factory.connection_lost(self, reason)
        else:
            self.factory.connection_done(self)

    def stringReceived(self, message):
        self.factory.read_message(self, message)

    def send_message(self, message):
        self.sendString(message)


class ProtocolServerFactory(Factory):
    protocol = Protocol

    def __init__(self, director):
        """
        :type director: L{im.services.facades.interfaces.IDirector}
        """
        self.director = director

    def connection_made(self, protocol):
        self.director.connection_made(protocol)

    def connection_lost(self, protocol, reason):
        self.director.connection_lost(protocol, reason)

    def connection_done(self, protocol):
        self.director.connection_done(protocol)

    def read_message(self, protocol, message):
        self.director.read_message(protocol, message)
