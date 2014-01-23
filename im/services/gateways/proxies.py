from pycloudia.services.interfaces import IInvoker
from pyschema import Schema, Str

from pycloudia.uitls.defer import inline_callbacks, return_value, deferrable
from pycloudia.uitls.structs import DataBean
from pycloudia.cluster.interfaces import IServiceAdapter
from pycloudia.cluster.beans import Activity

from im.services.gateways.interfaces import IService
from im.services.gateways.consts import HEADER, COMMAND, SERVICE, SOURCE


class RequestCreateSchema(Schema):
    client_id = Str()
    facade_id = Str()


class RequestDeleteSchema(Schema):
    client_id = Str()
    reason = Str()


class RequestAuthenticateSchema(Schema):
    client_id = Str()
    user_id = Str()


class ClientProxy(IService, IServiceAdapter):
    """
    :type sender: L{pycloudia.cluster.interfaces.ISender}
    """
    sender = None

    def __init__(self, source):
        """
        :type source: L{pycloudia.cluster.beans.Activity}
        """
        self.source = source

    def suspend_activity(self, activity):
        raise NotImplementedError()

    def recover_activity(self, activity):
        raise NotImplementedError()

    def create_gateway(self, client_id, facade_address):
        request = RequestCreateSchema().encode(DataBean(client_id=client_id, facade_id=facade_address))
        return self._send_request_package(client_id, COMMAND.CREATE, request)

    def delete_gateway(self, client_id, reason=None):
        request = RequestDeleteSchema().encode(DataBean(client_id=client_id, reason=reason))
        return self._send_request_package(client_id, COMMAND.DELETE, request)

    def authenticate_gateway(self, client_id, user_id):
        request = RequestAuthenticateSchema().encode(DataBean(client_id=client_id, user_id=user_id))
        return self._send_request_package(client_id, COMMAND.AUTHENTICATE, request)

    @deferrable
    def _send_request_package(self, client_id, command, request):
        target = self._create_target_activity(client_id)
        package = self.sender.package_factory(request, {
            HEADER.INTERNAL.COMMAND: command,
        })
        return self.sender.send_request_package(self.source, target, package)

    def process_incoming_package(self, client_id, package):
        return self._send_package(client_id, SOURCE.EXTERNAL, package)

    def process_outgoing_package(self, client_id, package):
        return self._send_package(client_id, SOURCE.INTERNAL, package)

    @deferrable
    def _send_package(self, client_id, source, package):
        target = self._create_target_activity(client_id)
        package.headers[HEADER.INTERNAL.SOURCE] = source
        package.headers[HEADER.INTERNAL.CLIENT_ID] = client_id
        self.sender.send_package(target, package)

    @staticmethod
    def _create_target_activity(client_id):
        return Activity(service=SERVICE.NAME, runtime=client_id)


class ServiceInvoker(IInvoker):
    """
    :type service_factory: C{Callable}
    """
    service_factory = None

    def __init__(self, channel):
        """
        :type channel: L{pycloudia.services.beans.Channel}
        """
        self.channel = channel
        self.service = None

    @deferrable
    def initialize(self):
        self.service = self.service_factory()
        self.service.runner_factory = self.create_runner_factory(self.channel)

    @deferrable
    def run(self):
        pass

    @deferrable
    def process_package(self, package):
        command = package.headers.pop(HEADER.INTERNAL.COMMAND, None)
        method = {
            COMMAND.CREATE: self._process_create_command,
            COMMAND.DELETE: self._process_delete_command,
            COMMAND.AUTHENTICATE: self._process_authenticate_command,
        }.get(command, self._forward_package)
        return method(package)

    @inline_callbacks
    def _process_create_command(self, package):
        request = RequestCreateSchema().decode(package.content)
        gateway = yield self.service.create_gateway(request.client_id, request.facade_id)
        return_value(package.create_response())

    @inline_callbacks
    def _process_delete_command(self, package):
        request = RequestDeleteSchema().decode(package.content)
        yield self.service.delete_gateway(request.client_id, request.reason)
        return_value(package.create_response())

    @inline_callbacks
    def _process_authenticate_command(self, package):
        request = RequestAuthenticateSchema().decode(package.content)
        yield self.service.authenticate_gateway(request.client_id, request.user_id)
        return_value(package.create_response())

    @deferrable
    def _forward_package(self, package):
        client_id = package.headers.pop(HEADER.INTERNAL.CLIENT_ID)
        source = package.headers.pop(HEADER.INTERNAL.SOURCE)
        if source == SOURCE.EXTERNAL:
            return self.service.process_incoming_package(client_id, package)
        elif source == SOURCE.INTERNAL:
            return self.service.process_outgoing_package(client_id, package)
        else:
            raise ValueError(source)
