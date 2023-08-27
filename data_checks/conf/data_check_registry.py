from data_checks.conf.settings import settings
from data_checks.utils import class_utils
from data_checks.classes.data_check import DataCheck


class DataCheckRegistry:
    def __init__(self):
        if settings["CHECKS_MODULE"] is None:
            raise ImportError("Please specify CHECKS_MODULE in your settings module.")
        else:
            checks = class_utils.classes_for_directory(
                settings["CHECKS_MODULE"],
                DataCheck,
            )

            self.checks: dict[str, type[DataCheck]] = {
                check.__name__: check for check in checks
            }
            self.keys = list(self.checks.keys())
            self.index = 0

    def __getitem__(self, item) -> type:
        return self.checks[item]

    def __str__(self) -> str:
        return f"{self.__dict__}"


data_check_registry = DataCheckRegistry()
