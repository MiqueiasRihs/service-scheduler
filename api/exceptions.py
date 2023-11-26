from rest_framework.exceptions import APIException
from rest_framework import status

class CustomValidation(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Um erro de validação ocorreu.'
    default_code = 'error'

    def __init__(self, detail, status_code):
        if status_code is not None:
            self.status_code = status_code
        if detail is not None:
            self.detail = {'message': detail}
