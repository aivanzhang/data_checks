from src.data_checks.dataset import Dataset
from src.data_checks.check import Check
from src.data_checks.rule import rule
from hamcrest import assert_that, equal_to
import pandas as pd
import os


class GeneralCompanyTransactionCheck(Check):
    def __init__(self, dataset: Dataset | None = None):
        super().__init__(dataset=dataset)
        self.description = "General Company Transaction Check"
        self.category = "Consistency"
        self.rules_params = {
            "company_payments_size_increasing": [
                {"args": (), "kwargs": {"company_name": "company_name"}},
                {"args": (), "kwargs": {"company_name": "company_name1"}},
                {"args": (), "kwargs": {"company_name": "company_name2"}},
                {"args": (), "kwargs": {"company_name": "company_name3"}},
                {"args": (), "kwargs": {"company_name": "company_name4"}},
                {"args": (), "kwargs": {"company_name": "company_name5"}},
                {"args": (), "kwargs": {"company_name": "company_name6"}},
            ],
            "company_payments_size_increasing_2": [
                {"args": (), "kwargs": {"company_name": "company_name7"}},
                {"args": (), "kwargs": {"company_name": "company_name8"}},
                {"args": (), "kwargs": {"company_name": "company_name9"}},
                {"args": (), "kwargs": {"company_name": "company_name10"}},
                {"args": (), "kwargs": {"company_name": "company_name11"}},
                {"args": (), "kwargs": {"company_name": "company_name12"}},
                {"args": (), "kwargs": {"company_name": "company_name13"}},
            ],
        }

    @staticmethod
    def should_run_rule():
        return False

    @rule(
        name="Company Payments Size Increasing",
        description="Size of the payments dataframe is increasing",
    )
    def company_payments_size_increasing(self, company_name, days=[2, 5]):
        # old_payments_df = pd.read_csv(
        #     os.path.dirname(os.path.realpath(__file__)) + "/old_payments.csv"
        # )
        # new_payments_df = pd.read_csv(
        #     os.path.dirname(os.path.realpath(__file__)) + "/new_payments.csv"
        # )
        print(company_name)
        assert_that(
            self.dataset.new_payments_df.shape[0]
            < self.dataset.old_payments_df.shape[0],
            equal_to(True),
            f"Size of the payments dataframe has decreased in the last few days",
        )

    @rule(
        name="Company Payments Size Increasing 2",
        description="Size of the payments dataframe is increasing",
    )
    def company_payments_size_increasing_2(self, company_name, days=[2, 5]):
        # old_payments_df = pd.read_csv(
        #     os.path.dirname(os.path.realpath(__file__)) + "/old_payments.csv"
        # )
        # new_payments_df = pd.read_csv(
        #     os.path.dirname(os.path.realpath(__file__)) + "/new_payments.csv"
        # )

        print(company_name)
        assert_that(
            self.dataset.new_payments_df.shape[0]
            >= self.dataset.old_payments_df.shape[0],
            equal_to(True),
            f"Size of the payments dataframe has decreased in the last few days",
        )
