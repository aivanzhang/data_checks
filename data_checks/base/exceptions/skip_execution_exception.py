"""
Exceptions for Skipping Data Checks
"""
from typing import Optional


class SkipExecutionException(Exception):
    """
    Raise this exception in an before action to skip the execution of a check
    """

    def __init__(
        self,
        reason: Optional[str] = None,
        metadata={},
    ):
        self.reason = reason
        self.metadata = metadata
        super().__init__()

    def __str__(self):
        return f"SkipExecutionException(reason={self.reason}, metadata={self.metadata})"
