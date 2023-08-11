from data_checks.conf.settings import settings
from data_checks.utils import class_utils


class Registry:
    checks = {}
    suites = {}

    def __init__(self):
        if settings["CHECKS_DIR"] is None:
            raise ImportError(
                "No checks found. Please specify CHECKS_DIR in your settings module."
            )
        else:
            check_classes = []
            self.checks = {
                check_class.__name__: check_class for check_class in check_classes
            }

        if settings["SUITES_DIR"] is None:
            raise ImportError(
                "No suites found. Please specify SUITES_DIR in your settings module."
            )
        else:
            suite_classes = []
            self.suites = {
                suite_class.__name__: suite_class for suite_class in suite_classes
            }

    def get_check(self, check_name):
        return self.checks[check_name]

    def get_suite(self, suite_name):
        return self.suites[suite_name]

    def __str__(self) -> str:
        return f"Registry(checks={self.checks}, suites={self.suites})"


registry = Registry()
