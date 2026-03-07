from scc.utils.schemas import ErrorCodes, ErrorSchema, ResponseSchema


def response(data=None, *, code: str = "", message: str = "") -> ResponseSchema:
    """
    Returns a response with the provided data, error, code, and message.

        Parameters:
            error (boolean): Indicate if there is an error or not
            code (str): Error code
            message (str): Information message
            data (dict): Additional data to be included in the response
            http_code (int): HTTP status code to return

        Returns:
            Json response to the sender
    """

    response_content = ResponseSchema(error=False, code=code, message=message, data=data)
    return response_content


def response_error(code: str = ErrorCodes.UNKNOWN_ERROR, message: str = "", data=None) -> ErrorSchema:
    """
    Returns a response with the provided data, error, code, and message.

        Parameters:
            error (boolean): Indicate if there is an error or not
            code (str): Error code
            message (str): Information message
            data (dict): Additional data to be included in the response
            http_code (int): HTTP status code to return

        Returns:
            Json response to the sender
    """

    response_content = ErrorSchema(error=True, code=code, message=message, data=data)
    return response_content
