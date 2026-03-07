from ninja_extra import NinjaExtraAPI

from authentication.api.versions.v1.api import AuthenticationController
from scc.utils.exceptions import AddApiExceptions

api = NinjaExtraAPI(version="1.0.0")

api.register_controllers(
    AuthenticationController,
)

AddApiExceptions(api)
