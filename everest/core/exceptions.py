from mountaineer import APIException


class NotFoundException(APIException):
    status_code = 404
    detail = "Detail item not found"
