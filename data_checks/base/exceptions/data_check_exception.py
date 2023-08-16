"""
Exceptions for Data Checks
"""
from typing import Optional
import json


class DataCheckException(Exception):
    """
    Exception raised for errors related to data checks.

    Attributes:
        severity = 1.0 -- severity of the error on a scale from 0 to 1
        exception -- exception that was raised
        metadata -- metadata related to the exception
    """

    def __init__(
        self,
        exception: Optional[Exception],
        severity=1.0,
        metadata={},
    ):
        self.severity = severity
        self.exception = exception
        self.metadata = metadata
        super().__init__()

    def __str__(self):
        return f"DataCheckException(severity={self.severity}, exception={self.exception}, metadata={self.metadata})"

    @classmethod
    def from_assertion_exception(
        cls, e: AssertionError, *args, **kwargs
    ) -> "DataCheckException":
        return cls(exception=e, *args, **kwargs)

    @classmethod
    def from_exception(cls, e, *args, **kwargs) -> "DataCheckException":
        return cls(exception=e, *args, **kwargs)

    def toJSON(self):
        return json.dumps(
            {
                "severity": self.severity,
                "exception": str(self.exception),
                "metadata": json.dumps(self.metadata, default=str),
            },
        )
