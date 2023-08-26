import pandas as pd
from examples.consumer.user_sign_up.checks.date_check import DataCheck
from examples.consumer.user_sign_up.checks.email_check import EmailCheck
from examples.consumer.user_sign_up.checks.ip_check import IpCheck
from examples.consumer.user_sign_up.checks.payments_check import PaymentsCheck
from examples.consumer.user_sign_up.checks.status_check import StatusCheck
from data_checks import DataSuite


class UserSuite(DataSuite):
    @classmethod
    def checks(cls):
        data = pd.read_csv("examples/consumer/user_sign_up/data.csv")
        return [
            DataCheck(dates_df=data),
            EmailCheck(emails=data["Email"]),
            IpCheck(ips=data["IP Address"]),
            PaymentsCheck(payments=data["Payment Amount"]),
            StatusCheck(statuses=data["Status"]),
        ]

    @classmethod
    def suite_config(cls) -> dict:
        return {
            "schedule": "* * * * *",
        }

    @classmethod
    def checks_overrides(cls) -> dict | None:
        return {
            "DateCheck": {
                # Run the format rule twice. Once for the default column, and once for the "Subscription Date" column
                "is_properly_formatted": [
                    {"format_pattern": r"\d{4}[-/]\d{2}[-/]\d{2}"},
                    {
                        "format_pattern": r"\d{4}[/]\d{2}[/]\d{2}",
                        "column": "Subscription Date",
                    },
                ],
                "within_range": [
                    # Check that the DOB is within the range of 18 to 200 years old
                    {
                        "start": pd.Timestamp.today()
                        - pd.DateOffset(
                            years=200
                        ),  # user can't be older than 200 years
                        "end": pd.Timestamp.today()
                        - pd.DateOffset(years=18),  # user must be at least 18 years old
                    },
                    # Check that the Subscription Date is within the range of today to the end of time
                    {
                        "column": "Subscription Date",
                        "start": pd.Timestamp.today(),
                        "end": pd.Timestamp.max,
                    },
                ],
            }
        }
