from ninja import Schema

from authentication.schemas import UserSchema


# region Requests schemas
class LoginRequestSchema(Schema):
    username: str
    password: str


class VerifyRequestSchema(Schema):
    access: str


# region Response schemas
class LoginResponseSchema(Schema):
    access: str
    user: UserSchema | None = None
