class SERVICE(object):
    NAME = 'gateways'


class COMMAND(object):
    CREATE = 'create'
    DELETE = 'delete'
    AUTHENTICATE = 'authorize'


class SOURCE(object):
    EXTERNAL = 'external'
    INTERNAL = 'internal'


class HEADER(object):
    INTERNAL_PREFIX = 'N-'

    class INTERNAL(object):
        REQUEST_ID = 'N-Request-Id'
        SOURCE = 'N-Clients-Source'
        USER_ID = 'N-Clients-User-Id'
        SERVICE = 'N-Router-Service'
        COMMAND = 'N-Router-Command'
        CLIENT_ID = 'N-Clients-Client-Id'
        AUTH_PLATFORM = 'N-Clients-Auth-Platform'
        AUTH_ACCESS_TOKEN = 'N-Clients-Auth-Access-Token'

    class EXTERNAL(object):
        RUNTIME = 'X-Runtime'
        SERVICE = 'X-Service'
        TIMEOUT = 'X-Timeout'
        REQUEST_ID = 'X-Request-Id'
        RESPONSE_ID = 'X-Response-Id'


class DEFAULT(object):
    class EXTERNAL(object):
        TIMEOUT = 30
