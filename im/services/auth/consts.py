class SERVICE(object):
    NAME = 'auth'


class HEADER(object):
    COMMAND = 'X-Auth-Command'
    USER_ID = 'X-Auth-User-Id'


class COMMAND(object):
    AUTHENTICATE = 'authenticate'


class VERBOSE(object):
    AUTHENTICATION_FAILED = 'authentication_failed'
