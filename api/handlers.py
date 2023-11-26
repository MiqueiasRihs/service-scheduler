from rest_framework.views import exception_handler

from api.exceptions import CustomValidation

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and isinstance(exc, CustomValidation):
        response.data = exc.detail

    return response
