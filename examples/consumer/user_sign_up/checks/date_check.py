import re
import pandas as pd
from data_checks import DataCheck
from hamcrest import assert_that, equal_to, is_not


class DateCheck(DataCheck):

    def rule_is_properly_formatted(self, format_pattern, column="DOB"):
        dates = self.dates_df[column]
        for date in dates:
            assert_that(
                re.match(format_pattern, date),
                is_not(None),
                f"Invalid date: {date}",
            )

    def rule_nonnull(self, column="DOB"):
        dates = self.dates_df[column]
        assert_that(dates.isnull().sum(), equal_to(0), "Null date found")

    def rule_valid_date(self, column="DOB"):
        dates = self.dates_df[column]
        for date in dates:
            assert_that(
                pd.to_datetime(date, errors="coerce"),
                is_not(pd.NaT),
                f"Invalid date: {date}",
            )

    def rule_within_range(self, start, end, column="DOB"):
        dates = self.dates_df[column]
        for date in dates:
            date = pd.to_datetime(date)
            if pd.isnull(date):
                continue
            assert_that(
                pd.Timestamp(start) <= date <= pd.Timestamp(end),
                equal_to(True),
                f"Date {date} is not within range {start} to {end}",
            )
