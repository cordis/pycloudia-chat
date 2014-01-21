class BaseFacadeError(Exception):
    pass


class ListenFailedError(BaseFacadeError):
    def __init__(self, host, port, *args, **kwargs):
        self.host = host
        self.port = port
        super(ListenFailedError, self).__init__(*args, **kwargs)

    def __str__(self):
        return 'Listening failed on {0}:{1}'.format(self.host, self.port)


class ClientNotFoundError(BaseFacadeError):
    def __init__(self, client_id, *args, **kwargs):
        self.client_id = client_id
        super(ClientNotFoundError, self).__init__(*args, **kwargs)
