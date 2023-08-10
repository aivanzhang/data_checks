from data_checks.base.check import Check
from data_checks.utils import class_utils


class DataCheck(Check):
    @classmethod
    def rules_prefix(cls) -> str | None:
        """
        Prefix to automatically detect rules in the check.
        """
        return None

    @classmethod
    def defined_rules(cls) -> list[str]:
        return class_utils.get_current_class_specific_methods(cls)
