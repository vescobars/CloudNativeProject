class ApiError(Exception):
    code = 422
    description = "Default message"


class Unauthorized(ApiError):
    code = 401
    description = "Unauthorized"


class IncompleteParams(ApiError):
    code = 400
    description = "Bad request"


class InvalidParamFormat(ApiError):
    code = 412
    description = "Bad request"


class InvalidParam(ApiError):
    code = 400
    description = "Bad param"


class OfferNotFoundError(ApiError):
    code = 404
    description = "Offer does not exist"


class ExternalError(ApiError):
    code = 422  # Default
    description = "External error"

    def __init__(self, code):
        self.code = code
