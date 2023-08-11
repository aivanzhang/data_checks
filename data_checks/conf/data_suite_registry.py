from data_checks.conf.settings import settings
from data_checks.utils import class_utils
from data_checks import DataSuite


class DataSuiteRegistry:
    def __init__(self):
        if settings["SUITES_MODULE"] is None:
            raise ImportError("Please specify SUITES_MODULE in your settings module.")
        else:
            suites = class_utils.classes_for_directory(
                settings["SUITES_MODULE"], DataSuite
            )

            for suite in suites:
                setattr(self, suite.__name__, suite)

    def __getitem__(self, item) -> type:
        return self.__dict__[item]

    def __str__(self) -> str:
        return f"{self.__dict__}"


data_suite_registry = DataSuiteRegistry()
