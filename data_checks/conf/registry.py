from data_checks.conf import settings
from data_checks.utils import class_utils
from data_checks.base.check_types import CheckBase
from data_checks.base.suite_types import SuiteBase


class Registry:
    checks = {}
    suites = {}

    def __init__(self):
        if settings["CHECKS_MODULE"] is None:
            raise ImportError(
                "No checks found. Please specify CHECKS_MODULE in your settings module."
            )
        else:
            check_classes = class_utils.classes_for_directory(
                settings["CHECKS_MODULE"], CheckBase
            )
            self.checks = {
                check_class.__name__: check_class for check_class in check_classes
            }

        if settings["SUITES_MODULE"] is None:
            raise ImportError(
                "No suites found. Please specify SUITES_MODULE in your settings module."
            )
        else:
            suite_classes = class_utils.classes_for_directory(
                settings["SUITES_MODULE"], SuiteBase
            )
            self.suites = {
                suite_class.__name__: suite_class for suite_class in suite_classes
            }

    def get_check(self, check_name):
        return self.checks[check_name]

    def get_suite(self, suite_name):
        return self.suites[suite_name]


registry = Registry()
