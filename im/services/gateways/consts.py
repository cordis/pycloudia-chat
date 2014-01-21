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
        SOURCE = 'N-Source'
        USER_ID = 'N-User-Id'
        COMMAND = 'N-Command'
        CLIENT_ID = 'N-Client-Id'
        REQUEST_ID = 'N-Request-Id'

    class EXTERNAL(object):
        SERVICE = 'X-Service'
        COMMAND = 'X-Command'
        RUNTIME = 'X-Runtime'
        TIMEOUT = 'X-Timeout'
        REQUEST_ID = 'X-Request-Id'
        RESPONSE_ID = 'X-Response-Id'


class DEFAULT(object):
    class EXTERNAL(object):
        TIMEOUT = 30
