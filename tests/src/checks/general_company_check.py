from data_checks.base.dataset import Dataset
from data_checks.base.rule import rule
from hamcrest import assert_that, equal_to
import pandas as pd
import os
from tests.src.checks.test_check import TestCheck


class GeneralCompanyTransactionCheck(TestCheck):
    def __init__(self, dataset: Dataset | None = None):
        super().__init__(dataset=dataset)
        self.description = "General Company Transaction Check"
        self.category = "Consistency"
        self.rules_params = {
            "company_payments_size_increasing": lambda: {
                "args": ("company_name1",),
                "kwargs": {"days": [4, 10]},
            },
            # [
            #     {
            #         "args": ("company_name1",),
            #         "kwargs": {"days": [4, 10]},
            #     },
            #     {
            #         "args": ("company_name2",),
            #     },
            #     {
            #         "args": ("company_name3",),
            #         "days": [6, 12],
            #     },
            #     ("company_name4", [10, 20]),
            # ]
            # ("company_name1", [4, 10]),
            # {
            #     "company_name": "company_name1",
            #     "days": [4, 10],
            # }
            # {
            #     "args": ("company_name1",),
            #     "kwargs": {"days": [4, 10]},
            # },
            # lambda: {
            #     "args": ("company_name1",),
            #     "kwargs": {"days": [4, 10]},
            # },
        }

    #         | Callable[
    #             ..., FunctionArgs  | list[Union[FunctionArgs, dict, tuple]]
    #         ]
    @classmethod
    def rules_prefix(cls):
        return ""

    @staticmethod
    def should_run_rule():
        return False

    @rule(
        name="Company Payments Size Increasing",
        description="Size of the payments dataframe is increasing",
    )
    def company_payments_size_increasing(
        self, company_name="company_name", days=[2, 5]
    ):
        # old_payments_df = pd.read_csv(
        #     os.path.dirname(os.path.realpath(__file__)) + "/old_payments.csv"
        # )
        # new_payments_df = pd.read_csv(
        #     os.path.dirname(os.path.realpath(__file__)) + "/new_payments.csv"
        # )
        print(company_name, days)
        assert_that(
            self.dataset.new_payments_df.shape[0]
            < self.dataset.old_payments_df.shape[0],
            equal_to(True),
            f"Size of the payments dataframe has decreased in the last few days",
        )

    # @rule(
    #     name="Company Payments Size Increasing 2",
    #     description="Size of the payments dataframe is increasing",
    # )
    # def company_payments_size_increasing_2(self, company_name, days=[2, 5]):
    #     # old_payments_df = pd.read_csv(
    #     #     os.path.dirname(os.path.realpath(__file__)) + "/old_payments.csv"
    #     # )
    #     # new_payments_df = pd.read_csv(
    #     #     os.path.dirname(os.path.realpath(__file__)) + "/new_payments.csv"
    #     # )

    #     print(company_name)
    #     assert_that(
    #         self.dataset.new_payments_df.shape[0]
    #         >= self.dataset.old_payments_df.shape[0],
    #         equal_to(True),
    #         f"Size of the payments dataframe has decreased in the last few days",
    #     )
