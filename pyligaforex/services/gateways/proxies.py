from pyschema import Schema, Str

from pycloudia.uitls.defer import inline_callbacks, return_value, deferrable
from pycloudia.uitls.structs import DataBean
from pycloudia.services.interfaces import IInvoker

from pyligaforex.services.consts import HEADER
from pyligaforex.services.gateways.consts import COMMAND, SOURCE
from pyligaforex.services.gateways.interfaces import IService


class RequestCreateSchema(Schema):
    service = Str()
    address = Str()
    runtime = Str()


class RequestDeleteSchema(Schema):
    runtime = Str()
    reason = Str()


class RequestAuthenticateSchema(Schema):
    runtime = Str()
    user_id = Str()


class ClientProxy(IService):
    """
    :type sender: L{pycloudia.cluster.interfaces.ISender}
    :type target_factory: L{pycloudia.services.interfaces.IServiceChannelFactory}
    """
    sender = None
    target_factory = None

    def __init__(self, source):
        """
        :type source: L{pycloudia.service.beans.Channel}
        """
        self.source = source

    def create_gateway(self, channel):
        request = RequestCreateSchema().encode(channel)
        return self._send_request_package(channel.runtime, COMMAND.CREATE, request)

    def delete_gateway(self, runtime, reason=None):
        request = RequestDeleteSchema().encode(DataBean(runtime=runtime, reason=reason))
        return self._send_request_package(runtime, COMMAND.DELETE, request)

    def authenticate_gateway(self, runtime, user_id):
        request = RequestAuthenticateSchema().encode(DataBean(runtime=runtime, user_id=user_id))
        return self._send_request_package(runtime, COMMAND.AUTHENTICATE, request)

    @deferrable
    def _send_request_package(self, runtime, command, request):
        target = self.target_factory.create_by_runtime(runtime)
        package = self.sender.package_factory(request, {
            HEADER.INTERNAL.COMMAND: command,
        })
        return self.sender.send_request_package(self.source, target, package)

    def process_incoming_package(self, runtime, package):
        return self._send_package(runtime, SOURCE.EXTERNAL, package)

    def process_outgoing_package(self, runtime, package):
        return self._send_package(runtime, SOURCE.INTERNAL, package)

    @deferrable
    def _send_package(self, runtime, source, package):
        target = self.target_factory.create_by_runtime(runtime)
        package.headers[HEADER.INTERNAL.SOURCE] = source
        package.headers[HEADER.INTERNAL.GATEWAY] = runtime
        self.sender.send_package(target, package)


class ServiceInvoker(IInvoker):
    """
    :type channel_factory: L{pycloudia.services.interfaces.IServiceChannelFactory}
    :type service_factory: L{pyligaforex.services.gateways.interfaces.IServiceFactory}
    :type runner_factory: L{pyligaforex.services.gateways.interfaces.IGatewayFactory}
    """
    channel_factory = None
    service_factory = None
    runner_factory = None

    def __init__(self, channel):
        """
        :type channel: L{pycloudia.services.beans.Channel}
        """
        self.channel = channel
        self.service = None

    @deferrable
    def initialize(self):
        self.service = self.service_factory.create_service()

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
        yield self.service.create_gateway(request)
        return_value(package.create_response())

    @inline_callbacks
    def _process_delete_command(self, package):
        request = RequestDeleteSchema().decode(package.content)
        yield self.service.delete_gateway(request.runtime, request.reason)
        return_value(package.create_response())

    @inline_callbacks
    def _process_authenticate_command(self, package):
        request = RequestAuthenticateSchema().decode(package.content)
        yield self.service.authenticate_gateway(request.runtime, request.user_id)
        return_value(package.create_response())

    @deferrable
    def _forward_package(self, package):
        runtime = package.headers.pop(HEADER.INTERNAL.GATEWAY)
        source = package.headers.pop(HEADER.INTERNAL.SOURCE)
        if source == SOURCE.EXTERNAL:
            return self.service.process_incoming_package(runtime, package)
        elif source == SOURCE.INTERNAL:
            return self.service.process_outgoing_package(runtime, package)
        else:
            raise ValueError(source)
