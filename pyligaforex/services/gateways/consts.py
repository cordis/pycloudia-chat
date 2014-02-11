class COMMAND(object):
    CREATE = 'create'
    DELETE = 'delete'
    AUTHENTICATE = 'authorize'


class SOURCE(object):
    EXTERNAL = 'external'
    INTERNAL = 'internal'


class DEFAULT(object):
    class EXTERNAL(object):
        TIMEOUT = 30
