"""AioOmada errors."""


class AioOmadaException(Exception):
    """Base error for aioomada."""


class RequestError(AioOmadaException):
    """Unable to fulfill request.

    Raised when host or API cannot be reached.
    """


class ResponseError(AioOmadaException):
    """Invalid response."""


class Unauthorized(AioOmadaException):
    """Username is not authorized."""


class LoginRequired(AioOmadaException):
    """User is logged out."""


class NoPermission(AioOmadaException):
    """Users permissions are read only."""


class ServiceUnavailable(RequestError):
    """Service is unavailable.

    Common error if controller is restarting and behind a proxy.
    """


class BadGateway(RequestError):
    """Invalid response from the upstream server."""


class TwoFaTokenRequired(AioOmadaException):
    """2 factor authentication token required."""


ERRORS = {
    "api.err.LoginRequired": LoginRequired,
    "api.err.Invalid": Unauthorized,
    "api.err.NoPermission": NoPermission,
    "api.err.Ubic2faTokenRequired": TwoFaTokenRequired,
}


def raise_error(error) -> None:
    """Raise error."""
    type = error
    cls = ERRORS.get(type, AioOmadaException)
    raise cls("{}".format(type))
