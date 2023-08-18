from data_checks.base.dataset import Dataset
from data_checks import DataCheck
from hamcrest import assert_that, equal_to
import pandas as pd
import os
import time


class TradeCheck2(DataCheck):
    def company_payments_size_increasing(
        self, company_name="company_name", days=[2, 5]
    ):
        print(company_name, days, self.trade)

    def company_payments_size_increasing_2(self, company_name="company_2"):
        print(company_name, self.trade)
