from data_checks.base.check import Check


class TestCheck(Check):
    test_str: str = "test"

    def setup(self):
        return super().setup()
