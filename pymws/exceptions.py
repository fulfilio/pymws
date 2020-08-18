"""
All errors and exceptions
"""


class MWSException(Exception):
    """
    Parent class of all exceptions this package handles
    """
    pass


class MWSError(MWSException):
    """
    Parent class of all Amazon returned Errors.
    """
    pass


class AccessDenied(MWSError):
    "Access was denied"


class SignatureDoesNotMatch(MWSError):
    """The signature used does not match the server's
    calculated signature value."""
    pass


class QuotaExceeded(MWSError):
    """The total number of requests in an hour was exceeded."""
    pass


class RequestThrottled(MWSError):
    """The frequency of requests was greater than allowed.."""
    pass
