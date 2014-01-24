from pycloudia.uitls.structs import DataBean
from pycloudia.uitls.defer import inline_callbacks, return_value, deferrable
from pycloudia.cluster.exceptions import PackageIgnoredWarning
from pycloudia.cluster.resolver import resolve_errors
from pycloudia.services.interfaces import IInvoker

from im.services.consts import HEADER
from im.services.auth.interfaces import IService
from im.services.auth.exceptions import Resolver
from im.services.auth.consts import COMMAND
from im.services.auth.schemas import AuthenticateRequestSchema, AuthenticateResponseSchema


class ServiceAdapter(IService):
    """
    :type sender: L{pycloudia.cluster.interfaces.ISender}
    :type target_factory: L{pycloudia.services.interfaces.IServiceChannelsFactory}
    """
    sender = None
    target_factory = None

    def __init__(self, source):
        """
        :type source: L{pycloudia.services.beans.Channel}
        """
        self.source = source

    @inline_callbacks
    def authenticate(self, client_id, platform, access_token):
        target = self.target_factory.create_by_runtime(client_id)
        request = self._create_request_package(client_id, platform, access_token)
        response = yield self.sender.send_request_package(self.source, target, request)
        profile = AuthenticateResponseSchema().decode(response.content)
        return_value(profile)

    def _create_request_package(self, client_id, platform, access_token):
        """
        :type client_id: C{str}
        :type platform: C{str}
        :type access_token: C{str}
        :rtype: L{pycloudia.packages.interfaces.IPackage}
        """
        request = DataBean(platform=platform, access_token=access_token)
        request = AuthenticateRequestSchema().encode(request)
        return self.sender.package_factory(request, {
            HEADER.INTERNAL.CLIENT_ID: client_id,
            HEADER.INTERNAL.COMMAND: COMMAND.AUTHENTICATE,
        })


class ServiceInvoker(IInvoker):
    """
    :type service_factory: C{im.services.auth.interfaces.IServiceFactory}
    :type users_factory: L{im.services.auth.interfaces.IUsersFactory}
    :type sessions_factory: L{im.services.auth.interfaces.ISessionsFactory}
    """
    service_factory = None
    users_factory = None
    sessions_factory = None

    def __init__(self, channel):
        """
        :type channel: L{pycloudia.services.beans.Channel}
        """
        self.channel = channel
        self.service = None

    @deferrable
    def initialize(self):
        self.service = self.service_factory.create_service()
        self.service.users = self.users_factory.create_adapter(self.channel)
        self.service.sessions = self.sessions_factory.create_adapter(self.channel)

    @deferrable
    def run(self):
        pass

    @deferrable
    def process_package(self, package):
        if COMMAND.AUTHENTICATE == package.headers.pop(HEADER.INTERNAL.COMMAND, None):
            return self._process_authenticate_request_package(package)
        raise PackageIgnoredWarning(package)

    @resolve_errors(Resolver)
    @inline_callbacks
    def _process_authenticate_request_package(self, package):
        """
        :type package: L{pycloudia.packages.interfaces.IRequestPackage}
        """
        client_id = package.headers[HEADER.INTERNAL.CLIENT_ID]
        request = AuthenticateRequestSchema().decode(package.content)
        profile = yield self.service.authenticate(client_id, request.platform, request.access_token)
        response = self._create_authenticate_response_package(package, profile)
        return_value(response)

    @staticmethod
    def _create_authenticate_response_package(request_package, profile):
        """
        :type request_package: L{pycloudia.cluster.interfaces.IRequestPackage}
        :type profile: L{im.services.auth.platforms.interfaces.IProfile}
        :rtype: L{pycloudia.packages.interfaces.IPackage}
        """
        response = AuthenticateResponseSchema().encode(profile)
        return request_package.create_response(response)
