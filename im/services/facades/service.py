from pycloudia.uitls.structs import BiDirectedDict
from pycloudia.uitls.defer import deferrable

from im.services.facades.exceptions import ClientNotFoundError
from im.services.facades.interfaces import IService, IDirector


class Service(IService, IDirector):
    """
    :type gateways: L{im.services.gateways.interfaces.IService}
    :type logger: L{im.services.facades.logger.Logger}
    :type encoder: L{pycloudia.packages.interfaces.IEncoder}
    :type decoder: L{pycloudia.packages.interfaces.IDecoder}
    :type listener: L{im.services.facades.interfaces.IListener}
    :type client_id_factory: C{im.services.facades.interfaces.IClientIdFactory}
    """
    gateways = None

    logger = None
    encoder = None
    decoder = None
    listener = None
    client_id_factory = None

    def __init__(self, address):
        """
        :type address: C{str}
        """
        self.address = address
        self.clients_map = BiDirectedDict()

    @deferrable
    def start(self):
        self.listener.start(self)

    def connection_made(self, client):
        self.clients_map[client] = client_id = self.client_id_factory()
        self.gateways.create_gateway(client_id, self.address)

    def connection_done(self, client):
        self.connection_lost(client, None)

    def connection_lost(self, client, reason):
        try:
            client_id = self.clients_map.pop(client)
        except KeyError:
            self.logger.log_client_not_found(client)
        else:
            self.gateways.delete_gateway(client_id, reason)

    def read_message(self, client, message):
        try:
            client_id = self.clients_map[client]
        except KeyError:
            self.logger.log_client_not_found(client)
        else:
            package = self.decoder.decode(message)
            self.gateways.process_incoming_package(client_id, package)

    def process_outgoing_package(self, address, client_id, package):
        assert address == self.address
        client = self._get_client_by_client_id(client_id)
        message = self.encoder.encode(package)
        client.send_message(message)

    def _get_client_by_client_id(self, client_id):
        """
        :type client_id: C{str}
        :rtype: L{im.services.facades.interfaces.IClient}
        :raise: L{im.services.facades.exceptions.ClientNotFoundError}
        """
        try:
            return self.clients_map.behind[client_id]
        except KeyError:
            raise ClientNotFoundError(client_id)
