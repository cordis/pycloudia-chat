from pyschema import Schema, Str, Unicode


class AuthenticateRequestSchema(Schema):
    platform = Str()
    access_token = Str()


class AuthenticateResponseSchema(Schema):
    user_id = Str()
    name = Unicode()
    email = Str()
    avatar = Str()
    birthday = Str()
