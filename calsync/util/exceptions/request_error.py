"""
Error class for when a request is invalid
"""

from calsync.util.exceptions.value_error_wrapper import ValueErrorWrapper


class RequestError(ValueErrorWrapper):
    pass
