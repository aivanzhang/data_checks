import os
import pandas as pd
from data_checks.base.dataset import Dataset
from data_checks import GroupDataSuite
from tests.src.checks.trade_check import TradeCheck
from tests.src.checks.trade_check_2 import TradeCheck2


class GroupedConsistencySuite(GroupDataSuite):
    @classmethod
    def dataset(cls) -> Dataset | None:
        return Dataset(
            {
                "test": 1
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
    def group_name(cls) -> str:
        """
        Identifier for each element in the group. Can be accessed through self.group_name in checks
        """
        return "trade"

    @classmethod
    def group(cls) -> list:
        """
        List of group's elements. Each element will be passed to the specified checks
        """
        return [1, 2, 3, 4, 5, 6, 7]

    @classmethod
    def group_checks(cls):
        """
        Checks to be run on each element in the group. For example:
        [
            CheckClass1,
            CheckClass2,
            ...
        ]
        with group
        [
            element1,
            element2,
            ...
        ]
        will run CheckClass1 on element1, CheckClass1 on element2, CheckClass2 on element1, and CheckClass2 on element2.
        """
        return [TradeCheck, TradeCheck2]

    # @classmethod
    # def suite_config(cls) -> dict:
    #     return {
    #         "schedule": "* * * * *",
    #     }

    # @classmethod
    # def checks_overrides(cls) -> dict | None:
    #     return {
    #         "GeneralCompanyTransactionCheck": {
    #             "company_payments_size_increasing": [
    #                 {
    #                     "company_name": "test",
    #                     "days": [50, 100],
    #                 },
    #                 {
    #                     "company_name": "test1",
    #                     "days": [51, 101],
    #                 },
    #                 {
    #                     "company_name": "test2",
    #                     "days": [52, 102],
    #                 },
    #             ],
    #             "company_payments_size_increasing_2": {
    #                 "company_name": "test",
    #                 "days": [100, 200],
    #             },
    #         }
    #     }
