import pandas as pd
from hamcrest import assert_that, greater_than_or_equal_to
from data_checks import DataCheck


class FreshnessCheck(DataCheck):
    def rule_ensure_all_fresh_data(self, date_column="date", max_days_stale=2):
        dates = pd.read_csv("examples/general/freshness/data.csv")[date_column]
        for date in dates:
            assert_that(
                pd.Timestamp(date),
                greater_than_or_equal_to(
                    pd.Timestamp("2023-08-22 10:00:00")
                    - pd.Timedelta(days=max_days_stale)
                ),
                f"Data is stale. The date {date} is older than {max_days_stale} days ago.",
            )
