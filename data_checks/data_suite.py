from data_checks.base.dataset import Dataset
from data_checks.base.check import Check
from data_checks.base.suite import Suite


class DataSuite(Suite):
    @classmethod
    def dataset(cls) -> Dataset:
        """
        Dataset that is shared across all checks in the suite. Use this to define all the data needed for this suite's checks. Accessed by rules via cls.dataset() or self.dataset()
        """
        raise NotImplementedError

    @classmethod
    def checks_overrides(cls) -> dict:
        """
        Overrides for check parameters. Dictionary should be in the following format:
        {
            CheckClass.rule_name: {
                "param1": value1,
                "param2": value2,
                ...
            },
            ...
        }
        """
        raise NotImplementedError

    @classmethod
    def checks_config(cls) -> dict:
        """
        Config that is shared across all checks in the suite. Use this to define all configuration details needed for this suite's checks. Accessed by rules via cls.config() or self.config()
        """
        raise NotImplementedError

    @classmethod
    def checks(cls) -> list[Check | str]:
        """
        Checks to be run by the suite. Can be specified by class or name (if CHECKS_DIR is defined) Each check should be a subclass of Check.
        """
        raise NotImplementedError
