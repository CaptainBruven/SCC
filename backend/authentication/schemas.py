from ninja import Schema


# region Model schemas
class UserSchema(Schema):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str | None
