from pycloudia.uitls.structs import DataBean


class Session(DataBean):
    service = None
    address = None
    runtime = None


class SessionsService(object):
    service = None

    @staticmethod
    def get_session_by_id(session_id):
        service, address, runtime = session_id.split(':')
        return Session(service=service, address=address, runtime=runtime)


class SessionsServiceFactory(object):
    def create_service(self):
        pass

    def create_adapter(self, source):
        pass
