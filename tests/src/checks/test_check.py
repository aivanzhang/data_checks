from data_checks.data_check import DataCheck


class TestCheck(DataCheck):
    test_str: str = "test"

    def setup(self):
        return super().setup()
