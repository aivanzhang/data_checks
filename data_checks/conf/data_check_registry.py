from data_checks.conf.settings import settings
from data_checks.utils import class_utils
from data_checks import DataCheck


class DataCheckRegistry:
    def __init__(self):
        if settings["CHECKS_MODULE"] is None:
            raise ImportError(
                "No checks found. Please specify CHECKS_MODULE in your settings module."
            )
        else:
            checks = class_utils.classes_for_directory(
                settings["CHECKS_MODULE"], DataCheck
            )
            for check in checks:
                setattr(self, check.__name__, check)

    def __getitem__(self, item) -> type:
        return self.__dict__[item]

    def __str__(self) -> str:
        return f"{self.__dict__}"


data_check_registry = DataCheckRegistry()
