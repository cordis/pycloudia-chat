class Service(object):
    def get_currency_list(self):
        raise NotImplementedError()

    def get_currency(self):
        raise NotImplementedError()


class ServiceFactory(object):
    pass
