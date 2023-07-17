"""
Exceptions for Data Checks
"""


class DataCheckException(Exception):
    """Exception raised for errors related to data checks.

    Attributes:
        severity = 1.0 -- severity of the error on a scale from 0 to 1
        exception -- exception that was raised
        metadata -- metadata related to the exception
    """

    def __init__(
        self,
        severity: float = 1.0,
        exception: Exception | None = None,
        metadata: dict = {},
    ):
        self.severity = severity
        self.exception = exception
        self.metadata = metadata
        super().__init__()
