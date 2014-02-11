class Logger(object):
    def __init__(self, subject):
        self.subject = subject

    def log_facade_not_found(self, facade_id):
        self.subject.warn('Facade `%s` not found', facade_id)
