class Logger(object):
    def __init__(self, subject):
        """
        :type subject: L{logging.Logger}
        """
        self.subject = subject

    def log_client_not_found(self, client):
        self.subject.warn('Client `%r` not found', client)

    def log_header_not_found(self, header_name):
        self.subject.warn('Header `%s` not found', header_name)
