from typing import Optional, TypedDict
from .database.managers import models


class SuiteInternal(TypedDict):
    """
    Internal suite data
    """

    suite_model: Optional[models.Suite]
