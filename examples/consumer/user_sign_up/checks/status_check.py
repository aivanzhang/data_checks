from data_checks.classes.data_check import DataCheck
from hamcrest import assert_that, equal_to, less_than_or_equal_to


class StatusCheck(DataCheck):
    def rule_valid_values(self):
        for status in self.statuses:
            assert_that(
                status in ["pending", "inactive", "active"],
                equal_to(True),
                f"Invalid status value: {status}",
            )

    def rule_majority_active_status(self):
        assert_that(
            self.statuses.value_counts().idxmax(),
            equal_to("active"),
            "Majority of statuses are not active",
        )

    def rule_minimal_inactive_and_pending_status(self):
        status_counts = self.statuses.value_counts()
        inactive_count = status_counts["inactive"]
        pending_count = status_counts["pending"]
        total_count = status_counts.sum()
        assert_that(
            inactive_count / total_count,
            less_than_or_equal_to(0.25),
            f"Inactive status is more than 25% of the dataset but found {inactive_count} out of {total_count} statuses",
        )
        assert_that(
            pending_count / total_count,
            less_than_or_equal_to(0.25),
            f"Pending status is more than 25% of the dataset but found {pending_count} out of {total_count} statuses",
        )
