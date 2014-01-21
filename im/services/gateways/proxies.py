from pycloudia.uitls.structs import DataBean
from pyschema import Schema, Str

from pycloudia.uitls.defer import inline_callbacks, return_value, deferrable
from pycloudia.cluster.interfaces import IServiceInvoker, IServiceAdapter
from im.services.gateways.interfaces import IService
from im.services.gateways.consts import HEADER, COMMAND, SERVICE, SOURCE


class RequestCreateSchema(Schema):
    client_id = Str()
    facade_id = Str()


class RequestDeleteSchema(Schema):
    client_id = Str()
    reason = Str()


class ClientProxy(IService, IServiceAdapter):
    def __init__(self, sender):
        """
        :type sender: L{pycloudia.cluster.interfaces.ISender}
        """
        self.sender = sender

    def create_gateway(self, client_id, facade_id):
        request = RequestCreateSchema().encode(DataBean(client_id=client_id, facade_id=facade_id))
        package = self.sender.package_factory(request, {
            HEADER.COMMAND: COMMAND.CREATE,
        })
        self.sender.send_package(client_id, SERVICE.NAME, package)

    def delete_gateway(self, client_id, reason=None):
        request = RequestDeleteSchema().encode(DataBean(client_id=client_id, reason=reason))
        package = self.sender.package_factory(request, {
            HEADER.COMMAND: COMMAND.DELETE,
        })
        self.sender.send_package(client_id, SERVICE.NAME, package)

    def suspend_activity(self, client_id):
        raise NotImplementedError()

    def recover_activity(self, client_id, facade_id):
        raise NotImplementedError()

    def authenticate_gateway(self, client_id, user_id):
        package = self.sender.package_factory({}, {
            HEADER.CLIENT_ID: client_id,
            HEADER.USER_ID: user_id,
            HEADER.COMMAND: COMMAND.AUTHENTICATE,
        })
        return self.sender.send_request_package(package)

    def process_incoming_package(self, client_id, package):
        package.headers[HEADER.SOURCE] = SOURCE.EXTERNAL
        package.headers[HEADER.CLIENT_ID] = client_id
        self.sender.send_package(client_id, SERVICE.NAME, package)

    def process_outgoing_package(self, client_id, package):
        package.headers[HEADER.SOURCE] = SOURCE.INTERNAL
        package.headers[HEADER.CLIENT_ID] = client_id
        self.sender.send_package(client_id, SERVICE.NAME, package)


class ServerProxy(IServiceInvoker):
    def __init__(self, service):
        """
        :type service: L{im.services.gateways.interfaces.IService}
        """
        self.service = service

    @deferrable
    def process_package(self, package):
        command = package.headers.pop(HEADER.COMMAND, None)
        method = {
            COMMAND.CREATE: self._process_create_command,
            COMMAND.DELETE: self._process_delete_command,
            COMMAND.AUTHENTICATE: self._process_authenticate_command,
        }.get(command, self._forward_package)
        return method(package)

    @deferrable
    def _process_create_command(self, package):
        request = RequestCreateSchema().decode(package.content)
        return self.service.create_gateway(request.client_id, request.facade_id)

    @deferrable
    def _process_delete_command(self, package):
        request = RequestDeleteSchema().decode(package.content)
        return self.service.delete_gateway(request.client_id, request.reason)

    @inline_callbacks
    def _process_authenticate_command(self, package):
        client_id = package.headers[HEADER.CLIENT_ID]
        user_id = package.headers[HEADER.USER_ID]
        yield self.service.authenticate_gateway(client_id, user_id)
        return_value(package.create_response())

    @deferrable
    def _forward_package(self, package):
        client_id = package.headers[HEADER.CLIENT_ID]
        source = package.headers[HEADER.SOURCE]
        if source == SOURCE.EXTERNAL:
            return self.service.process_incoming_package(client_id, package)
        elif source == SOURCE.INTERNAL:
            return self.service.process_outgoing_package(client_id, package)
        else:
            raise ValueError(source)
