from typing import Optional
from src.data_checks.base.dataset import Dataset
from src.data_checks.base.check import Check
from src.data_checks.base.suite import Suite


class UserDefinedSuite(Suite):
    @classmethod
    def dataset(cls) -> Optional[Dataset]:
        """
        Get the dataset for the suite
        """
        raise NotImplementedError

    @classmethod
    def shared_params(cls) -> Optional[dict]:
        """
        Get the shared parameters for the suite's checks
        """
        raise NotImplementedError

    @classmethod
    def checks(cls) -> list[Check]:
        """
        Get all checks in the suite
        """
        raise NotImplementedError
