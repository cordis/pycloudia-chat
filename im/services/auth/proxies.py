from pycloudia.uitls.structs import DataBean
from pycloudia.uitls.defer import inline_callbacks, return_value, deferrable
from pycloudia.cluster.interfaces import IServiceInvoker
from pycloudia.cluster.exceptions import PackageIgnoredWarning
from pycloudia.cluster.resolver import resolve_errors
from pycloudia.cluster.beans import Activity

from im.services.gateways.consts import HEADER as GATEWAY_HEADER
from im.services.auth.interfaces import IService
from im.services.auth.exceptions import Resolver
from im.services.auth.consts import HEADER, COMMAND, SERVICE
from im.services.auth.schemas import AuthenticateRequestSchema, AuthenticateResponseSchema


class ClientProxy(IService):
    """
    :type sender: L{pycloudia.cluster.interfaces.ISender}
    """
    sender = None

    def __init__(self, source):
        """
        :type source: L{pycloudia.cluster.beans.Activity}
        """
        self.source = source

    @inline_callbacks
    def authenticate(self, client_id, platform, access_token):
        target = self._create_target(client_id)
        request = self._create_request_package(client_id, platform, access_token)
        response = yield self.sender.send_request_package(self.source, target, request)
        profile = AuthenticateResponseSchema().decode(response.content)
        return_value(profile)

    @staticmethod
    def _create_target(client_id):
        """
        :type client_id: C{str}
        :rtype: L{pycloudia.cluster.beans.Activity}
        """
        return Activity(service=SERVICE.NAME, runtime=client_id)

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
            HEADER.COMMAND: COMMAND.AUTHENTICATE,
            GATEWAY_HEADER.INTERNAL.CLIENT_ID: client_id,
        })


class ServerProxy(IServiceInvoker):
    def __init__(self, service):
        """
        :type service: L{im.services.auth.interfaces.IService}
        """
        self.service = service

    @deferrable
    def process_package(self, package):
        if COMMAND.AUTHENTICATE == package.headers.pop(HEADER.COMMAND, None):
            return self._process_authenticate_request_package(package)
        raise PackageIgnoredWarning(package)

    @resolve_errors(Resolver)
    @inline_callbacks
    def _process_authenticate_request_package(self, package):
        client_id = package.headers[GATEWAY_HEADER.INTERNAL.CLIENT_ID]
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
        return request_package.create_response(response, {
            HEADER.USER_ID: profile.user_id,
        })
