from abc import ABCMeta, abstractmethod, abstractproperty


class IService(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_thread_messages(self, actor, thread, limit=None, offset=None):
        """
        :type actor: L{pyligaforex.services.chats.interfaces.IActor}
        :type thread: L{pyligaforex.services.chats.interfaces.IChatIdentity}
        :type limit: C{int} or C{None}
        :type offset: C{str} or C{None}
        """

    @abstractmethod
    def create_thread_message(self, actor, thread, content):
        """
        :type actor: L{pyligaforex.services.chats.interfaces.IActor}
        :type thread: L{pyligaforex.services.chats.interfaces.IChatIdentity}
        :type content: L{pyligaforex.services.chats.interfaces.IChatMessageContent}
        """

    @abstractmethod
    def update_thread_message(self, actor, thread, message_id, content):
        """
        :type actor: L{pyligaforex.services.chats.interfaces.IActor}
        :type thread: L{pyligaforex.services.chats.interfaces.IChatIdentity}
        :type message_id: C{str}
        :type content: L{pyligaforex.services.chats.interfaces.IChatMessageContent}
        """

    @abstractmethod
    def delete_thread_message(self, actor, thread, message_id):
        """
        :type actor: L{pyligaforex.services.chats.interfaces.IActor}
        :type thread: L{pyligaforex.services.chats.interfaces.IChatIdentity}
        :type message_id: C{str}
        """

    def grant_thread_access(self):
        raise NotImplementedError()


class IActor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_id(self):
        """
        :rtype: C{str}
        """

    @abstractmethod
    def is_authenticated(self):
        """
        :rtype: C{bool}
        """


class IChatIdentity(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __str__(self):
        """
        :rtype: C{str}
        """


class IChatMessageContent(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def text(self):
        """
        :rtype: C{unicode}
        """
