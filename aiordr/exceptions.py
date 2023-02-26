"""
This module contains custom exception types.
"""
from __future__ import annotations

from .models import ErrorCode

__all__ = ("APIException",)


class APIException(Exception):
    """API Exception Class

    :param status: status code from the API
    :type status: int
    :param message: error message returned
    :type message: str
    :param error_code: error code returned
    :type error_code: aiordr.models.errorcode.ErrorCode
    """

    def __init__(self, status: int, message: str, error_code: ErrorCode) -> None:
        super().__init__(message)
        self.status = status
        self.error_code = error_code

    @property
    def message(self) -> str:
        """Error message returned by the API

        :return: Error message
        :rtype: str
        """
        return self.args[0]
