import logging

from springpython.config import Object
from springpython.context import scope

from pycloudia.ioc_config import Config


class ChatConfig(Config):
    @Object(scope.PROTOTYPE)
    def bootstrap(self):
        from chat.bootstrap import ChatBootstrap
        instance = ChatBootstrap()
        instance.logger = logging.getLogger('bootstrap')
        instance.device_one = self.device()
        instance.device_two = self.device()
        instance.starter = self.starter()
        return instance

    @Object(scope.SINGLETON)
    def identity_factory(self):
        if self.options.identity is None:
            return super(ChatConfig, self).identity_factory()
        return lambda: self.options.identity
