from mountaineer.exceptions import APIException


class UnauthorizedError(APIException):
    status_code = 302
    detail = "You're not authorized to access this resource."
    headers = {"Location": "/login"}
