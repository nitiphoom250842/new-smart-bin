
import os
from fastapi import HTTPException
from starlette import status


def unauthorized(http_method: str = 'GET'):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        headers=generate_common_header_response(http_method),
    )


def not_found(http_method: str = 'GET'):
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        headers=generate_common_header_response(http_method),
    )


def bad_request(http_method: str = 'GET'):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        headers=generate_common_header_response(http_method),
    )


def generate_common_header_response(http_method: str):
    return {
        "Access-Control-Allow-Origin": os.getenv('WEB_URL'),
        "Access-Control-Allow-Credentials": "true",
        "Access-Control-Request-Method": http_method,
    }
