from typing import Optional, TypedDict
from .database.managers import models
from .dataset import Dataset


class SuiteInternal(TypedDict):
    """
    Internal suite data
    """

    suite_model: Optional[models.Suite]
    dataset: Optional[Dataset]
