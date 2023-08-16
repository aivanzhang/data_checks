import os
import pandas as pd
from data_checks.base.dataset import Dataset
from data_checks import DataSuite
from tests.src.checks.general_company_check import GeneralCompanyTransactionCheck


class ConsistencySuite(DataSuite):
    @classmethod
    def checks(cls) -> list[type]:
        return [
            GeneralCompanyTransactionCheck,
            # GeneralCompanyTransactionCheck,
        ]

    @classmethod
    def dataset(cls) -> Dataset | None:
        return Dataset(
            {
                # "old_payments_df": pd.read_csv(
                #     os.path.dirname(os.path.realpath(__file__)) + "/old_payments.csv"
                # ),
                # "new_payments_df": pd.read_csv(
                #     os.path.dirname(os.path.realpath(__file__)) + "/new_payments.csv"
                # ),
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
            "GeneralCompanyTransactionCheck": {
                "company_payments_size_increasing": [
                    {
                        "company_name": "test",
                        "days": [50, 100],
                    },
                    {
                        "company_name": "test1",
                        "days": [51, 101],
                    },
                    {
                        "company_name": "test2",
                        "days": [52, 102],
                    },
                ],
                "company_payments_size_increasing_2": {
                    "company_name": "test",
                    "days": [100, 200],
                },
            }
        }
