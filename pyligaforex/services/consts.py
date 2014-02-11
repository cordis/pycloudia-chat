class HEADER(object):
    class EXTERNAL(object):
        SERVICE = 'X-Service'
        COMMAND = 'X-Command'
        RUNTIME = 'X-Runtime'
        TIMEOUT = 'X-Timeout'
        REQUEST_ID = 'X-Request-Id'
        RESPONSE_ID = 'X-Response-Id'

    class INTERNAL(object):
        SOURCE = 'N-Source'
        COMMAND = 'N-Command'
        USER_ID = 'N-User-Id'
        GATEWAY = 'N-Gateway'
