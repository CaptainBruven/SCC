from http import HTTPStatus

from django.contrib.auth import authenticate, get_user_model
from django.http import HttpRequest, HttpResponse
from ninja.constants import NOT_SET
from ninja_extra import api_controller, route
from ninja_jwt.tokens import AccessToken, RefreshToken

from scc.utils.responses import response, response_error
from scc.utils.schemas import ErrorCodes, ErrorSchema, ResponseSchema

from .schemas import LoginRequestSchema, LoginResponseSchema, UserSchema, VerifyRequestSchema


@api_controller("/", auth=NOT_SET, permissions=[])
class AuthenticationController:
    @route.post("/login", response={HTTPStatus.OK: ResponseSchema[LoginResponseSchema], HTTPStatus.UNAUTHORIZED: ErrorSchema})
    def login(self, request: HttpRequest, res: HttpResponse, data: LoginRequestSchema):
        user = authenticate(username=data.username, password=data.password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            access = AccessToken.for_user(user)

            response_data = LoginResponseSchema(
                access=str(access),
                user=UserSchema(
                    id=user.id,
                    email=user.email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                    username=user.username,
                ),
            )

            res.set_cookie("refresh", str(refresh), httponly=True, secure=True, max_age=86400, samesite="None")
            return HTTPStatus.OK, response(data=response_data)

        return HTTPStatus.UNAUTHORIZED, response_error(code=ErrorCodes.WRONG_CREDENTIALS)

    @route.post(
        "/refresh",
        response={
            HTTPStatus.OK: ResponseSchema[LoginResponseSchema],
            HTTPStatus.BAD_REQUEST: ErrorSchema,
            HTTPStatus.UNAUTHORIZED: ErrorSchema,
            HTTPStatus.NOT_FOUND: ErrorSchema,
        },
    )
    def refresh(self, request: HttpRequest):
        refresh_token = request.COOKIES.get("refresh")

        if not refresh_token:
            return HTTPStatus.BAD_REQUEST, response_error(code=ErrorCodes.MISSING_REFRESH_TOKEN)

        try:
            refresh = RefreshToken(refresh_token)
            refresh.verify()
        except Exception as e:
            return HTTPStatus.UNAUTHORIZED, response_error(code=ErrorCodes.BLACKLISTED_TOKEN, message=str(e))

        try:
            user = refresh.payload.get("user_id")

            if not get_user_model().objects.filter(id=user).exists():
                return HTTPStatus.NOT_FOUND, response_error(code=ErrorCodes.USER_NOT_FOUND)

            user_obj = get_user_model().objects.get(id=user)
            access = AccessToken.for_user(user_obj)

            response_data = LoginResponseSchema(access=str(access))

            return HTTPStatus.OK, response(data=response_data)

        except Exception as e:
            return HTTPStatus.UNAUTHORIZED, response_error(code=ErrorCodes.INVALID_REFRESH_TOKEN, message=str(e))

    @route.post("/verify", response={HTTPStatus.OK: ResponseSchema, HTTPStatus.BAD_REQUEST: ErrorSchema, HTTPStatus.UNAUTHORIZED: ErrorSchema})
    def verify(self, request: HttpRequest, data: VerifyRequestSchema):
        access_token = data.access
        refresh_token = request.COOKIES.get("refresh")

        if not refresh_token:
            return HTTPStatus.BAD_REQUEST, response_error(code=ErrorCodes.MISSING_REFRESH_TOKEN)

        if not access_token:
            return HTTPStatus.BAD_REQUEST, response_error(code=ErrorCodes.MISSING_ACCESS_TOKEN)

        try:
            RefreshToken(refresh_token).verify()
        except Exception as e:
            return HTTPStatus.UNAUTHORIZED, response_error(code=ErrorCodes.BLACKLISTED_TOKEN, message=str(e))

        try:
            AccessToken(access_token).verify()
        except Exception as e:
            return HTTPStatus.UNAUTHORIZED, response_error(code=ErrorCodes.EXPIRED_TOKEN, message=str(e))

        return HTTPStatus.OK, response()

    @route.post("/logout", response={HTTPStatus.OK: ResponseSchema, HTTPStatus.BAD_REQUEST: ErrorSchema, HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema})
    def logout(self, request: HttpRequest):
        refresh_token = request.COOKIES.get("refresh")

        if not refresh_token:
            return HTTPStatus.BAD_REQUEST, response_error(code=ErrorCodes.MISSING_REFRESH_TOKEN)

        try:
            refresh = RefreshToken(refresh_token)
            refresh.verify()
        except Exception as e:
            return HTTPStatus.BAD_REQUEST, response_error(code=ErrorCodes.INVALID_REFRESH_TOKEN, message=str(e))

        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
            return HTTPStatus.OK, response()
        except Exception as e:
            return HTTPStatus.INTERNAL_SERVER_ERROR, response_error(message=str(e))
