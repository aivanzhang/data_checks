from data_checks.base.check import Check


class DataCheck(Check):
    @classmethod
    def rules_prefix(cls) -> str:
        """
        Prefix to automatically detect rules in the check
        """
        raise NotImplementedError
