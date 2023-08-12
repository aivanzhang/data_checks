from typing import Iterable, Tuple
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
            self.suites: dict[str, type[DataSuite]] = {
                suite.__name__: suite for suite in suites
            }
            self.keys = list(self.suites.keys())
            self.index = 0

    def __getitem__(self, item) -> type:
        return self.suites[item]

    def __str__(self) -> str:
        return ",".join(self.suites.keys())

    def __iter__(self):
        return self

    def __next__(self) -> Tuple[str, type]:
        if self.index >= len(self.keys):
            raise StopIteration
        else:
            key = self.keys[self.index]
            self.index += 1
            return key, self[key]

    def __len__(self):
        return len(self.keys)


data_suite_registry = DataSuiteRegistry()
