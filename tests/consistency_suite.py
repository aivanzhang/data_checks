from src.data_checks.suite import Suite
from .general_company_check import GeneralCompanyTransactionCheck


class ConsistencySuite(Suite):
    def __init__(self):
        super().__init__()
        self.name = "Consistency Suite"
        self.description = "Suite with checks that ensure consistency between different different transaction data stores"
        self.checks = [GeneralCompanyTransactionCheck()]
