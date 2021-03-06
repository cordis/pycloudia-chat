import logging

from springpython.config import Object
from springpython.context import scope

from pycloudia.ioc_config import Config


class ChatConfig(Config):
    @Object(scope.SINGLETON)
    def bootstrap(self):
        from pyligaforex.bootstrap import ChatBootstrap
        instance = ChatBootstrap()
        instance.logger = logging.getLogger('bootstrap')
        instance.device = self.device()
        instance.device_two = self.device()
        instance.starter = self.starter()
        return instance

    @Object(scope.SINGLETON)
    def identity(self):
        if self.options.identity is not None:
            return self.options.identity
        return super(ChatConfig, self).identity()

    @Object(scope.SINGLETON)
    def tcp_facade_service(self):
        from uuid import uuid4
        from pycloudia.activities.facades.service import Service
        from pycloudia.activities.facades.logger import Logger
        from pycloudia.activities.facades.twisted_impl.listeners import TcpListener
        instance = Service(self.identity)
        instance.logger = Logger(logging.getLogger('pyligaforex.facade'))
        instance.encoder = self.package_factory().create_encoder()
        instance.decoder = self.package_factory().create_decoder()
        instance.listener = TcpListener(self.localhost())
        instance.client_id_factory = lambda: str(uuid4())
        instance.sessions = self.gateways_service_adapter_factory()(instance.get_activity())
        return instance

    @Object(scope.SINGLETON)
    def gateway_service(self):
        from pyligaforex.services.gateways.service import Service
        instance = Service()
        instance.reactor = self.isolated_reactor()
        instance.gateway_factory = self.gateway_runner_factory()
        return instance

    @Object(scope.SINGLETON)
    def gateway_runner_factory(self):
        from pyligaforex.services.gateways.gateway import GatewayFactory
        from pyligaforex.services.gateways.dao import Dao
        instance = GatewayFactory()
        instance.dao = Dao()
        instance.sender = self.cluster_runner()
        instance.facades = self.facades_service_adapter()
        return instance

    @Object(scope.SINGLETON)
    def auth_service(self):
        from pyligaforex.services.auth.service import Service
        from pyligaforex.services.auth.dao import Dao
        instance = Service(self.identity)
        instance.reactor = self.isolated_reactor()
        instance.dao = Dao()
        instance.platforms = self.auth_platform_adapter_registry()
        instance.sessions = self.gateways_service_adapter_factory()(instance.get_activity())
        instance.users = self.users_service_adapter_factory()(instance.get_activity())
        return instance

    @Object(scope.SINGLETON)
    def auth_platform_adapter_registry(self):
        from pyligaforex.services.auth.consts import PLATFORM
        from pyligaforex.services.auth.platforms.registry import Registry
        return Registry({
            PLATFORM.BOTS: self.bots_auth_platform_adapter(),
        })

    @Object(scope.SINGLETON)
    def bots_auth_platform_adapter(self):
        from pyligaforex.services.auth.platforms.bots.adapter import Adapter
        return Adapter()
