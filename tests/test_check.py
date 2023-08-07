from src.data_checks.check import Check


class TestCheck(Check):
    test_str: str = "test"

    def setup(self):
        print("HI")
        return super().setup()
