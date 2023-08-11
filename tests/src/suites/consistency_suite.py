import os
import pandas as pd
from data_checks.base.suite import Suite
from data_checks.base.dataset import Dataset
from tests.src.checks.general_company_check import GeneralCompanyTransactionCheck


class ConsistencySuite(Suite):
    def __init__(self):
        super().__init__()
        self.name = "Consistency Suite"
        self.description = "Suite with checks that ensure consistency between different different transaction data stores"
        # self.dataset = Dataset({"old_payments_df": None, "new_payments_df": None})
        # Dataset(
        #     {
        #         "old_payments_df": pd.read_csv(
        #             os.path.dirname(os.path.realpath(__file__)) + "/old_payments.csv"
        #         ),
        #         "new_payments_df": pd.read_csv(
        #             os.path.dirname(os.path.realpath(__file__)) + "/new_payments.csv"
        #         ),
        #     }
        # )

        self.checks = []
        # [
        #     GeneralCompanyTransactionCheck(),
        #     GeneralCompanyTransactionCheck(),
        #     GeneralCompanyTransactionCheck(),
        #     GeneralCompanyTransactionCheck(),
        #     GeneralCompanyTransactionCheck(),
        # ]

        # for check in self.checks:
        #     check.use_dataset(self.dataset)
