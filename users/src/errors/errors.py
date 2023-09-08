class ApiError(Exception):
    code = 422
    description = "Default message"


class UserAlreadyExists(ApiError):
    code = 412
    description = "User with username or email already exists"


class UserNotFoundError(ApiError):
    code = 404
    description = "User with username and password does not exist"


class IncompleteParams(ApiError):
    code = 400
    description = "Bad request"


class NotToken(ApiError):
    code = 403
    description = "You need to specify a auth token"


class Unauthorized(ApiError):
    code = 401
    description = "Unauthorized"
