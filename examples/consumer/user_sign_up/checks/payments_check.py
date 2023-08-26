import re
from data_checks import DataCheck
from hamcrest import assert_that, equal_to, is_not


class PaymentsCheck(DataCheck):
    def rule_positive_payments(self):
        payments = self.dataset["data"]["Payment Amount"]
        for payment in payments:
            assert_that(
                payment > 0,
                equal_to(True),
                f"Payment value is not positive: {payment}",
            )

    def rule_payments_numeric_values(self):
        payments = self.dataset["data"]["Payment Amount"]
        for payment in payments:
            assert_that(
                isinstance(payment, (int, float)),
                equal_to(True),
                f"Payment value is not numeric: {payment}",
            )

    def rule_payments_not_null(self):
        payments = self.dataset["data"]["Payment Amount"]
        for payment in payments:
            assert_that(
                payment,
                is_not(None),
                f"Payment value is null: {payment}",
            )

    def rule_payments_less_than(self, value=100):
        payments = self.dataset["data"]["Payment Amount"]
        for payment in payments:
            assert_that(
                payment < value,
                equal_to(True),
                f"Payment value is not less than {value}: {payment}",
            )
