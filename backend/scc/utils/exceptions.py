import traceback
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import PermissionDenied
from ninja.errors import AuthenticationError

from scc.utils.error_codes import ErrorCodes
from scc.utils.responses import response_error


def AddApiExceptions(api):
    @api.exception_handler(AuthenticationError)
    def validation_errors(request, exc: AuthenticationError):
        print(request.user, request, exc)
        return api.create_response(request=request, data=response_error(ErrorCodes.UNAUTHORIZED, message=str(exc)), status=HTTPStatus.UNAUTHORIZED)

    @api.exception_handler(PermissionDenied)
    def permission_error(request, exc: PermissionError):
        return api.create_response(request=request, data=response_error(ErrorCodes.UNAUTHORIZED, message=str(exc)), status=HTTPStatus.FORBIDDEN)

    @api.exception_handler(Exception)
    def unknown_errors(request, exc: Exception):
        if settings.DEBUG:
            print(traceback.format_exc())
        else:
            # capture_exception(exc)
            pass
        return api.create_response(request=request, data=response_error(ErrorCodes.UNKNOWN_ERROR, message=str(exc)), status=HTTPStatus.INTERNAL_SERVER_ERROR)
