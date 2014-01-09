from abc import ABCMeta, abstractmethod, abstractproperty


class IService(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_private_threads(self, actor, frame):
        """
        :type actor: C{im.services.im.interfaces.IActor}
        :type frame: C{im.services.im.interfaces.IFrame}
        """

    @abstractmethod
    def get_thread_messages(self, actor, thread, frame):
        """
        :type actor: C{im.services.im.interfaces.IActor}
        :type thread: C{im.services.im.interfaces.IThreadIdentity}
        :type frame: C{im.services.im.interfaces.IFrame}
        """

    @abstractmethod
    def create_thread_message(self, actor, thread, content):
        """
        :type actor: C{im.services.im.interfaces.IActor}
        :type thread: C{im.services.im.interfaces.IThreadIdentity}
        :type content: C{im.services.im.interfaces.IThreadMessageContent}
        """

    @abstractmethod
    def update_thread_message(self, actor, thread, message_id, content):
        """
        :type actor: C{im.services.im.interfaces.IActor}
        :type thread: C{im.services.im.interfaces.IThreadIdentity}
        :type message_id: C{str}
        :type content: C{im.services.im.interfaces.IThreadMessageContent}
        """

    @abstractmethod
    def delete_thread_message(self, actor, thread, message_id):
        """
        :type actor: C{im.services.im.interfaces.IActor}
        :type thread: C{im.services.im.interfaces.IThreadIdentity}
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


class IThreadIdentity(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __str__(self):
        """
        :rtype: C{str}
        """


class IThreadMessageContent(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def text(self):
        """
        :rtype: C{unicode}
        """


class IFrame(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def limit(self):
        """
        :rtype: C{int} or C{None}
        """

    @abstractproperty
    def offset(self):
        """
        :rtype: C{str} or C{None}
        """
