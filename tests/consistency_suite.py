import os
import pandas as pd
from src.data_checks.suite import Suite
from src.data_checks.dataset import Dataset
from .general_company_check import GeneralCompanyTransactionCheck


class ConsistencySuite(Suite):
    def __init__(self):
        super().__init__()
        self.name = "Consistency Suite"
        self.description = "Suite with checks that ensure consistency between different different transaction data stores"
        self.dataset = Dataset(
            "Payments Dataset",
            old_payments_df=pd.read_csv(
                os.path.dirname(os.path.realpath(__file__)) + "/old_payments.csv"
            ),
            new_payments_df=pd.read_csv(
                os.path.dirname(os.path.realpath(__file__)) + "/new_payments.csv"
            ),
        )

        self.checks = [GeneralCompanyTransactionCheck()]

        # for check in self.checks:
        #     check.use_dataset(self.dataset)
