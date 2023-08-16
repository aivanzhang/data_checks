from data_checks.base.dataset import Dataset
from data_checks.base.suite import Suite


class DataSuite(Suite):
    @classmethod
    def dataset(cls) -> Dataset | None:
        """
        Dataset that is shared across all checks in the suite. Use this to define all the data needed for this suite's checks. Accessed by rules via cls.dataset() or self.dataset()
        """
        return None

    @classmethod
    def checks_overrides(cls) -> dict | None:
        """
        Overrides for check parameters. Dictionary should be in the following format:
        {
            "CheckClass": {
                "rule_1": {
                    "param1": value1,
                    "param2": value2,
                    ...
                },
                "rule_2": {
                    "param1": value1,
                    "param2": value2,
                    ...
                }
                ...
            },
            "..."
        }
        """
        return None

    @classmethod
    def suite_config(cls) -> dict:
        """
        System configurations for the suite. In the following format:
        {
            "schedule": "0 8 * * *", # cron schedule for the suite
        }
        """
        return {
            "schedule": "0 8 * * *",  # default to run every day at 8am
        }

    @classmethod
    def checks(cls) -> list[type | str]:
        """
        Checks to be run by the suite. Can be specified by class. Each check should be a subclass of Check.
        """
        raise NotImplementedError
