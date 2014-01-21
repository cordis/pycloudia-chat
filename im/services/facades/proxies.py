from im.services.facades.interfaces import IService
from im.services.facades.consts import SERVICE, HEADER
from pycloudia.cluster.interfaces import IServiceInvoker


class ClientProxy(IService):
    def __init__(self, sender):
        """
        :type sender: L{pycloudia.cluster.interfaces.ISender}
        """
        self.sender = sender

    def process_outgoing_package(self, address, client_id, package):
        package.headers[HEADER.FACADE_ID] = address
        package.headers[HEADER.CLIENT_ID] = client_id
        self.sender.send_package(address, SERVICE.NAME, package)


class ServerProxy(IServiceInvoker):
    def __init__(self, service):
        """
        :type service: L{im.services.facades.interfaces.IService}
        """
        self.service = service

    def process_package(self, package):
        facade_id = package.headers.pop(HEADER.FACADE_ID)
        client_id = package.headers.pop(HEADER.CLIENT_ID)
        self.service.process_outgoing_package(facade_id, client_id, package)
