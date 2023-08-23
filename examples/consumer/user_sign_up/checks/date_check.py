import re
import pandas as pd
from data_checks import DataCheck
from hamcrest import assert_that, equal_to, is_not


class DateCheck(DataCheck):
    def is_properly_formatted(self, format_pattern):
        dates = self.dataset["data"]["DOB"]
        for date in dates:
            assert_that(
                re.match(format_pattern, date),
                is_not(None),
                f"Invalid date: {date}",
            )

    def nonnull(self):
        dates = self.dataset["data"]["DOB"]
        assert_that(dates.isnull().sum(), equal_to(0), "Null date found")

    def valid_date(self):
        dates = self.dataset["data"]["DOB"]
        for date in dates:
            assert_that(
                pd.to_datetime(date, errors="coerce"),
                is_not(pd.NaT),
                f"Invalid date: {date}",
            )

    def within_range(self, start, end):
        dates = self.dataset["data"]["DOB"]
        for date in dates:
            date = pd.to_datetime(date)
            if pd.isnull(date):
                continue
            assert_that(
                pd.Timestamp(start) <= date <= pd.Timestamp(end),
                equal_to(True),
                f"Date {date} is not within range {start} to {end}",
            )
