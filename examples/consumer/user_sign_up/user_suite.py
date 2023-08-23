import pandas as pd
from data_checks.base.dataset import Dataset
from data_checks import DataSuite


class UserSuite(DataSuite):
    @classmethod
    def checks(cls):
        return ["EmailCheck", "DateCheck"]

    @classmethod
    def dataset(cls) -> Dataset | None:
        return Dataset(
            {
                "data": pd.read_csv("examples/consumer/user_sign_up/data.csv"),
            }
        )

    @classmethod
    def suite_config(cls) -> dict:
        return {
            "schedule": "* * * * *",
        }

    @classmethod
    def checks_overrides(cls) -> dict | None:
        return {
            "DateCheck": {
                "is_properly_formatted": {"format_pattern": r"\d{4}[-/]\d{2}[-/]\d{2}"},
                "within_range": {
                    "start": pd.Timestamp.today()
                    - pd.DateOffset(years=120),  # user can't be older than 120 years
                    "end": pd.Timestamp.today()
                    - pd.DateOffset(years=18),  # user must be at least 18 years old
                },
            }
        }
