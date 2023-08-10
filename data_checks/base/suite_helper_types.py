from typing import Optional, TypedDict
from data_checks.base.dataset import Dataset
from data_checks.database.managers import models


class SuiteInternal(TypedDict):
    """
    Internal suite data
    """

    suite_model: Optional[models.Suite]
    suite_execution_model: Optional[models.SuiteExecution]
    dataset: Optional[Dataset]
    shared_params: Optional[dict]
