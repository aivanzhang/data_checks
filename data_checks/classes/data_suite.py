from data_checks.conf.settings import settings
from data_checks.base.check import Check
from data_checks.base.suite import Suite


class DataSuite(Suite):
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
        You can also pass in an array to run a rule multiple times with
        different parameters. For example:
        {
            "CheckClass": {
                "rule_1": [
                    {
                        "param1": value1,
                        "param2": value2,
                        ...
                    },
                    {
                        "param1": value3,
                        "param2": value4,
                        ...
                    }
                ]
            }
        }
        runs rule_1 twice with different parameters.
        """
        return None

    @classmethod
    def suite_config(cls) -> dict:
        """
        Define the suite's configuration. This will be stored in the database.
        You can attach any configuration option as long as it is JSON serializable.
        `schedule` is the only system defined configuration option that defines the
        CRON schedule for the suite. For example:
        """
        return {
            "schedule": settings["DEFAULT_SCHEDULE"],  # default to run every day at 8am
        }

    @classmethod
    def checks(cls) -> list[type | str | Check]:
        """
        Checks to be run by the suite. Can be specified by class. Each check should be a subclass of Check.
        """
        raise NotImplementedError
